import argparse


functions = {}


def parse_source_section(section: list[str]):
    print("found source")
    print(functions)
    source_file = section[0].split()[-1]
    print(source_file)

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