import subprocess
import argparse
import tempfile
import os
import shutil

from parse_annoted import handle_logic

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("test_runs", help="A path to the file containing all test runs that you want to use")
    parser.add_argument("ddiasm", help="A path to the dissassembled binary likely using ddiasm")
    args = parser.parse_args()
    test_runs = args.test_runs
    temporary_dir = tempfile.mkdtemp()
    print(f"Creating a tempoary directory \"{temporary_dir}\" If this program exits abnormnally this directoy might not be removed")
    # Run cachegrind
    runs = []
    bin_name = None
    with open(test_runs) as f:
        run = f.readline()
        run_no = 0
        while run != "":
            run_split = run.strip().split()
            run_file = os.path.join(temporary_dir, f"run{run_no}")
            runs.append(run_file)
            cur_binary = run_split[0]
            if bin_name is None:
                bin_name = cur_binary
            assert bin_name == cur_binary, "multiple binary names detected, seperate your test runs"

            print(f"Running \"{run.strip()}\" using cachegrind. This may take a while")
            command_line = ["valgrind", "--tool=cachegrind", f"--cachegrind-out-file={run_file}", "--cache-sim=yes"]
            command_line.extend(run_split)
            complete_cachegrind = subprocess.run(command_line, capture_output=True)
            try:
                complete_cachegrind.check_returncode()
            except subprocess.CalledProcessError:
                print("Cachegrind seems to have failed in its work, printing error code")
                print(complete_cachegrind.stderr)
                shutil.rmtree(temporary_dir)
                exit(1)
            run_no += 1
            run = f.readline()
        if run_no == 0:
            raise AssertionError("Empty test runs file")
    print("Finished gathering data")
    # New we annotate
    command_line = ["cg_annotate", "--context=100000", "--no-show-percs"]
    command_line.extend(runs)

    annotate_file_name = os.path.join(temporary_dir, "annotation")
    with open(annotate_file_name, "wb+") as f:
        complete_annotation = subprocess.run(command_line, stdout=f, stderr=subprocess.PIPE)
    try: 
        complete_annotation.check_returncode()
    except subprocess.CalledProcessError:
        print("Somehow cachegrind annotate seems to have failed")
        print(complete_cachegrind.stderr)
        shutil.rmtree(temporary_dir)
        exit(1)


    # We also need to run objdump on it

    command_line = ["objdump", "-dS", bin_name]
    objdump_file_name = os.path.join(temporary_dir, "dump")
    with open(objdump_file_name, "wb+") as f:
        objdump = subprocess.run(command_line, stdout=f, check=True)

    print("Adding the prefetch instructions") 
    handle_logic(cachegrind=annotate_file_name, objdump=objdump_file_name, ddiasm=args.ddiasm)
    shutil.rmtree(temporary_dir)

    



if __name__ == "__main__":
    main()