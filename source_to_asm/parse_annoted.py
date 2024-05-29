import argparse
from dataclasses import dataclass
from typing import Optional
import re
from re import Match


@dataclass
class InstrumentedSource:
    source: str
    instruction_reads: Optional[int] = None
    i1_misses: Optional[int] = None
    ill_misses: Optional[int] = None
    data_reads: Optional[int] = None
    data_1_read_miss: Optional[int] = None
    data_ll_read_miss: Optional[int] = None
    data_writes: Optional[int] = None
    data_1_write_miss: Optional[int] = None
    data_ll_write_miss: Optional[int] = None


functions = {}
example = None


def parse_function(function: list[str], function_name: str):
    function_lines = []
    global example
    for line in function:
        line = " " + line
        line_split = line.split()
        ir = line_split[0]
        if ir == ".":
            ir = None
        else:
            ir = int(ir.replace(",", ""))

        i1_miss = line_split[1]
        if i1_miss == ".":
            i1_miss = None
        else:
            i1_miss = int(i1_miss.replace(",", ""))

        ill_miss = line_split[2]
        if ill_miss == ".":
            ill_miss = None
        else:
            ill_miss = int(ill_miss.replace(",", ""))

        data_reads = line_split[3]
        if data_reads == ".":
            data_reads = None
        else:
            data_reads = int(data_reads.replace(",", ""))

        data1_miss_reads = line_split[4]
        if data1_miss_reads == ".":
            data1_miss_reads = None
        else:
            data1_miss_reads = int(data1_miss_reads.replace(",", ""))

        datall_miss_reads = line_split[5]
        if datall_miss_reads == ".":
            datall_miss_reads = None
        else:
            datall_miss_reads = int(datall_miss_reads.replace(",", ""))

        data_writes = line_split[6]
        if data_writes == ".":
            data_writes = None
        else:
            data_writes = int(data_writes.replace(",", ""))

        data1_miss_writes = line_split[7]
        if data1_miss_writes == ".":
            data1_miss_writes = None
        else:
            data1_miss_writes = int(data1_miss_writes.replace(",", ""))

        datall_miss_writes = line_split[8]
        if datall_miss_writes == ".":
            datall_miss_writes = None
        else:
            datall_miss_writes = int(datall_miss_writes.replace(",", ""))
        source_line = " ".join(line_split[9:])
        instrumented_line = InstrumentedSource(
            source=source_line,
            instruction_reads=ir,
            i1_misses=i1_miss,
            ill_misses=ill_miss,
            data_reads=data_reads,
            data_1_read_miss=data1_miss_reads,
            data_ll_read_miss=datall_miss_reads,
            data_writes=data_writes,
            data_1_write_miss=data1_miss_writes,
            data_ll_write_miss=datall_miss_writes,
        )
        function_lines.append(instrumented_line)
        if example is None and datall_miss_reads is not None and datall_miss_reads != 0:
            example = instrumented_line
    functions[function_name] = function_lines


def parse_source_section(section: list[str]):
    # If we find a // @prefetch and it is in section, we know that we need
    # To add prefetch instructions here
    prefetch_lines = []
    prefetch_ctr = 0
    source_idx = 0
    for line in section:
        if "// @prefetch" in line:
            prefetch_lines.append(prefetch_ctr)
            if source_idx == 0:
                source_idx = line.find("// @prefetch")
        prefetch_ctr += 1
    for idx, line in enumerate(prefetch_lines):
        true_line = line + 1
        source_line = section[true_line][source_idx:]
        function_name = source_line.split()[1].split("(")[0]
        function_end = true_line
        if idx + 1 == len(prefetch_lines):
            function_end = len(section) - 1
        else:
            function_end = prefetch_lines[idx + 1]
        if function_name in functions:
            parse_function(section[true_line:function_end], function_name)


def parse_function_file_section(section: list[str]) -> dict[str, str]:
    char_num = section[1].find("function:file")
    global functions
    functions = {}
    for line in section[3::2]:
        funciton_file = line[char_num:]
        colon_split = funciton_file.split(":")
        function_name = colon_split[0]
        file_path = ":".join(colon_split[1:])
        functions[function_name] = file_path


def parse_section(section: list[str]):
    if not section:
        return
    if "-- Annotated source file: " in section[0]:
        parse_source_section(section)
    if "-- Function:file summary" in section[0]:
        return parse_function_file_section(section)


def determine_bad_load(
    source_line: InstrumentedSource, assembly_line: str
) -> Optional[Match]:
    # Given a source line of code, and the binary lone of code, returns the memory address
    # Register of the load that is badly made. If there assembly line does not
    # Access meemoy returns None

    if "(" not in assembly_line:
        return None
    if "lea" in assembly_line or "nop" in assembly_line:
        return None
    if type(source_line) == str:
        return None
    if source_line.data_1_read_miss is None:
        return None
    if source_line.data_ll_read_miss * 5 > source_line.data_reads:
        # Not enough misses here, try again later
        return None
    return re.search(r"\(.*\)", assembly_line)


def parse_objdump_function(
    function_name: str, function_body: list[str]
) -> tuple[list[str], list[int]]:
    if function_name not in functions:
        return ([], [])

    asm_pattern = re.compile(r"    [0-9a-f]*:\t.*")
    current_source = None
    idx = -2
    matching_asm = []
    my_function = functions[function_name]
    lines_of_source = {}
    fake_memory_operation = 0
    addresses = []
    memory_operations = []
    for line in function_body:
        stripped_line = line.strip("\n")
        match = re.match(asm_pattern, stripped_line)
        if match is None:
            if line in lines_of_source:
                idx = lines_of_source[line]
            else:
                matching_asm = []
                idx += 1
                lines_of_source[line] = idx
            current_source = stripped_line
        else:
            matching_asm.append(line)
            if current_source is None:
                print("No source???")
            if idx < 0:
                print("Dealing with offsets")
            else:
                if "(" in line:
                    fake_memory_operation += 1

                match = determine_bad_load(my_function[idx], line)
                if match is not None:
                    addresses.append(match[0])
                    memory_operations.append(fake_memory_operation)
    return (addresses, memory_operations)


def parse_basic_block(
    basic_block_lines: list[str],
    mem_operation_start: int,
    address: list[str],
    prefetch_locations: list[int],
) -> list[str]:
    # Parse the basic block and inset a prefetch instruction if needed
    # To inset a prefetch instruction we need to know which memory operations we need a prefetch for
    # The starting memoy instruction index, and the address to prefetch
    # Returns the rewritten basic block
    copy_basic_block = []
    cur_mem_operation = mem_operation_start
    memory_block = []
    for line in basic_block_lines:
        memory_block.append(line)
        if "(" in line:
            for idx, location in enumerate(prefetch_locations):
                if location > cur_mem_operation:
                    break
                if location == cur_mem_operation:
                    address_to_use = address[idx]
                    prefetch_instruction = " ".join(
                        ["            PREFETCHT1 ", address_to_use, "\n"]
                    )
                    memory_block.insert(0, prefetch_instruction)
                    break
            cur_mem_operation += 1
            copy_basic_block.extend(memory_block)
            memory_block = []
    copy_basic_block.extend(memory_block)
    return copy_basic_block


def parse_ddiasm_function(
    function_lines: list[str],
    function_name: str,
    memory_addeesses: list[str],
    memory_indexes: list[int],
):
    if function_name not in functions:
        return function_lines
    basic_block = []
    function_with_prefetch = []
    mem_operation = 0
    for line in function_lines:
        if line.startswith("."):
            function_with_prefetch.extend(
                parse_basic_block(
                    basic_block, mem_operation, memory_addeesses, memory_indexes
                )
            )
            basic_block = [line]
        else:
            basic_block.append(line)
        if "(" in line:
            mem_operation += 1
    function_with_prefetch.extend(basic_block)
    return function_with_prefetch


def write_function(f, lines):
    for line in lines:
        f.write(line)


def handle_logic(cachegrind, objdump, ddiasm):
    filename = cachegrind
    section = []
    count = 0
    with open(filename) as f:
        line = "junk"
        while line != "":
            line = f.readline()
            if (
                "---------------------------------------------------------------------------"
                in line
            ):
                count += 1
                if count == 3:
                    parse_section(section)
                    section = []
                    count = 1
            else:
                section.append(line)
    parse_section(section)

    # We have parsed the source code, now we want to parse the objdump
    filename = objdump
    cur_function_name = ""
    cur_function = []
    function_pattern = re.compile(r"[0-9a-f]{16} <.*>:")
    function_addresses = {}
    function_indexes = {}
    with open(filename) as f:
        line = "junk"
        while line != "":
            line = f.readline()
            if re.match(function_pattern, line):
                # do something with cur_function
                addresses, memory_indexes = parse_objdump_function(
                    cur_function_name, cur_function
                )
                function_addresses[cur_function_name] = addresses
                function_indexes[cur_function_name] = memory_indexes
                cur_function_name = line.split("<")[1].split(">")[0]
                cur_function = []
            else:
                cur_function.append(line)

        addresses, memory_indexes = parse_objdump_function(
            cur_function_name, cur_function
        )
        function_addresses[cur_function_name] = addresses
        function_indexes[cur_function_name] = memory_indexes

    # Now time to add the prefetch instructions

    filename = ddiasm
    ddiasm_func_pattern = re.compile(r"\.type .*, @function")
    cur_function = []
    cur_function_name = None
    out_file_name = ddiasm + "with_prefetch.s"
    with open(filename, "r") as f:
        with open(out_file_name, "w+") as w:
            line = "junk"
            f.seek(0)
            while line != "# end section .text\n":
                line = f.readline()
                if re.match(ddiasm_func_pattern, line.strip("\n")):
                    if cur_function_name is not None:
                        if cur_function_name in function_addresses:
                            my_addresses = function_addresses[cur_function_name]
                            my_indexes = function_indexes[cur_function_name]
                            new_function = parse_ddiasm_function(
                                cur_function,
                                cur_function_name,
                                my_addresses,
                                my_indexes,
                            )
                            cur_function = new_function
                    write_function(w, cur_function)
                    cur_function = [line]
                    cur_function_name = line.split()[1][:-1]
                else:
                    cur_function.append(line)
            cur_function = cur_function[:-1]  # Remvoe the end section .text
            if cur_function_name in function_addresses:
                my_addresses = function_addresses[cur_function_name]
                my_indexes = function_indexes[cur_function_name]
                new_function = parse_ddiasm_function(
                    cur_function, cur_function_name, my_addresses, my_indexes
                )
                cur_function = new_function
            write_function(w, cur_function)
            cur_function = []
            while line != "":
                cur_function.append(line)

                line = f.readline()
            write_function(w, cur_function)
