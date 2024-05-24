import argparse
import re

functions = {}


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
        print(function_name)
        if (function_name in functions):
            print(f"found {function_name}")
        function_end = true_line
        if (idx + 1 == len(prefetch_lines)):
            function_end = len(section) - 1
        else:
            function_end = prefetch_lines[idx + 1]
            print("Non last number")
        print(true_line, function_end)
        print(f"ending is {section[function_end]}")



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
    if ("-- Annotated source file: " in section[0]):
        parse_source_section(section)
    if ("-- Function:file summary" in section[0]):
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
        while(line != ""):
            # print(line)
            line = f.readline()
            if ("---------------------------------------------------------------------------" in line):
                count += 1
                if (count == 3):

                    parse_section(section)
                    section = []
                    count = 1
            else:
                section.append(line)
    parse_section(section)




if __name__ == "__main__":
    main()