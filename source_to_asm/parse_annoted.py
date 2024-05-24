import argparse
from dataclasses import dataclass
from typing import Optional


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


def parse_function(function: list[str]):
    print("________ NEW __________")
    function_lines = []
    for line in function:
        line = " " + line
        line_split = line.split()
        ir = line_split[0]
        if ir == ".":
            ir = None
        else:
            ir = int(ir)

        i1_miss = line_split[1]
        if i1_miss == ".":
            i1_miss = None
        else:
            i1_miss = int(i1_miss)

        ill_miss = line_split[2]
        if ill_miss == ".":
            ill_miss = None
        else:
            ill_miss = int(ill_miss)

        data_reads = line_split[3]
        if data_reads == ".":
            data_reads = None
        else:
            data_reads = int(data_reads)

        data1_miss_reads = line_split[4]
        if data1_miss_reads == ".":
            data1_miss_reads = None
        else:
            data1_miss_reads = int(data1_miss_reads)

        datall_miss_reads = line_split[5]
        if datall_miss_reads == ".":
            datall_miss_reads = None
        else:
            datall_miss_reads = int(datall_miss_reads)

        data_writes = line_split[6]
        if data_writes == ".":
            data_writes = None
        else:
            data_writes = int(data_writes)

        data1_miss_writes = line_split[7]
        if data1_miss_writes == ".":
            data1_miss_writes = None
        else:
            data1_miss_writes = int(data1_miss_writes)

        datall_miss_writes = line_split[8]
        if datall_miss_writes == ".":
            datall_miss_writes = None
        else:
            datall_miss_writes = int(datall_miss_writes)
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
    pass


def parse_source_section(section: list[str]):
    print("found source")
    print(functions)
    source_file = section[0].split()[-1]
    print(source_file)
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
            parse_function(section[true_line:function_end])
        # print(true_line, function_end)
        # print(f"ending is {section[function_end]}")


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
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


if __name__ == "__main__":
    main()
