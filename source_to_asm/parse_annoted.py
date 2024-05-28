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
    print("________ NEW __________")
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
            print("Set example")
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
    print(prefetch_lines)
    for idx, line in enumerate(prefetch_lines):
        true_line = line + 1
        source_line = section[true_line][source_idx:]
        function_name = source_line.split()[1].split("(")[0]
        # print(function_name)
        function_end = true_line
        if idx + 1 == len(prefetch_lines):
            function_end = len(section) - 1
        else:
            function_end = prefetch_lines[idx + 1]
            # print("Non last number")
        if function_name in functions:
            print(f"found {function_name}")
            parse_function(section[true_line:function_end], function_name)


def parse_function_file_section(section: list[str]) -> dict[str, str]:
    print("Found function::file")
    char_num = section[1].find("function:file")
    global functions
    functions = {}
    for line in section[3::2]:
        funciton_file = line[char_num:]
        print(funciton_file)
        colon_split = funciton_file.split(":")
        function_name = colon_split[0]
        file_path = ":".join(colon_split[1:])
        functions[function_name] = file_path


def parse_section(section: list[str]):
    print("---    NEW SECTION      ---")
    # print(section)
    if not section:
        return
    if "-- Annotated source file: " in section[0]:
        parse_source_section(section)
    if "-- Function:file summary" in section[0]:
        return parse_function_file_section(section)




def determine_bad_load(source_line: InstrumentedSource, assembly_line: str) -> Optional[Match]:
    # Given a source line of code, and the binary lone of code, returns the memory address 
    # Register of the load that is badly made. If there assembly line does not 
    # Access meemoy returns None

    if ("(" not in assembly_line):
        return None 
    if ("lea" in assembly_line or "nop" in assembly_line):
        return None
    # if (source_line.data_1_read_miss is None):
    #     return None
    # if (source_line.data_ll_read_miss * 5 > source_line.data_reads):
    #     # Not enough misses here, try again later
    #     return None
    return re.search(r"\(.*\)", assembly_line)
    
    


def parse_objdump_function(function_name: str, function_body: list[str]):
    print(f"{function_name=}")
    if function_name not in functions:
        print(f"Skipped {function_name}")
        return
    asm_pattern = re.compile(r"    [0-9a-f]*:\t.*")
    current_source = None
    idx = -2
    matching_asm = []
    my_function = functions[function_name]
    for line in function_body:
        stripped_line = line.strip("\n")
        match = re.match(asm_pattern, stripped_line)
        if match is None:
            if idx >= len(my_function):
                print(f"Souce fell off {current_source=}, {idx=}")
            else: 
                print(f"{current_source=}, {idx=}, {my_function[idx].source=}")
            current_source = stripped_line
            matching_asm = []
            idx += 1
        else:
            matching_asm.append(line)
            if (current_source is None):
                print("No source???")
            if (idx < 0):
                print("Dealing with offsets")
            if (idx >= len(my_function)):
                print("Fell off end somehow")
            else:
                match = determine_bad_load(my_function[idx], line)
                # print(f" {idx=}, {my_function[idx].source=}, {line=}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cachegrind")
    parser.add_argument("objdump")
    args = parser.parse_args()
    filename = args.cachegrind
    print(filename)
    section = []
    count = 0
    with open(filename) as f:
        line = "junk"
        while line != "":
            # print(line)
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

    # print(functions)

    # We have parsed the source code, now we want to parse the objdump
    filename = args.objdump
    cur_function_name = ""
    cur_function = []
    function_pattern = re.compile(r"[0-9a-f]{16} <.*>:")
    with open(filename) as f:
        line = "junk"
        while line != "":
            line = f.readline()
            if re.match(function_pattern, line):
                # do something with cur_function
                parse_objdump_function(cur_function_name, cur_function)
                cur_function_name = line.split("<")[1].split(">")[0]
                cur_function = []
            else:
                cur_function.append(line)

    # The fini section shoukd be at the end, so we dont really need to deal with it
    global example
    print(example)
    objdump_line = r"12e2:	48 c7 44 c7 f8 01 00 	movq   $0x1,-0x8(%rdi,%rax,8)"
    match = re.match(r"\(.*\)", objdump_line)
    print(objdump_line, match)
    print(match[0])
    


if __name__ == "__main__":
    main()
