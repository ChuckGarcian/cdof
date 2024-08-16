import subprocess
import argparse
import tempfile
import os
import shutil

from parse_annotated import handle_logic

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_runs", help="A path to the file containing all test runs that you want to use")
    parser.add_argument("ddisasm", help="A path to ddisasm disassembled binary")
    args = parser.parse_args()
    test_runs = args.test_runs
    temporary_dir = tempfile.mkdtemp()
    print(f"cdof: Creating a temporary directory \"{temporary_dir}\" If this program exits abnormally this directory might not be removed")
    
    # Run cachegrind
    runs = []        # 
    bin_path = None  #
    bin_name = None 
    
    with open(test_runs) as f:
        test_run_cmd = f.readline()
        run_no = 0
    
        while test_run_cmd != "":
            # Process and validate test run
            run_split = test_run_cmd.strip().split()
            run_file = os.path.join(temporary_dir, f"run{run_no}") # Cachegrind output file
            runs.append(run_file)       
            cur_binary = run_split[0] 
        
            if bin_path is None:
                bin_path = cur_binary
                bin_name = os.path.split(bin_path)[-1]
            assert bin_path == cur_binary, "multiple binary names detected, seperate your test runs"

            # Run Cachegrind
            print(f"cdof: Running \"{test_run_cmd.strip()}\" using cachegrind. This may take a while")
            command_line = ["valgrind", "--tool=cachegrind", f"--cachegrind-out-file={run_file}", "--cache-sim=yes"]
            command_line.extend(run_split)
            cachegrind_output = subprocess.run(command_line, capture_output=True)

            # Check Errors Running
            try:
                cachegrind_output.check_returncode()
            except subprocess.CalledProcessError:
                print("cdof: Cachegrind seems to have failed in its work, printing error code")
                print(cachegrind_output.stderr)
                shutil.rmtree(temporary_dir)
                exit(1)
        
            run_no += 1
            test_run_cmd = f.readline()
    
        if run_no == 0:
            raise AssertionError("Empty test runs file")

    print("Finished gathering data")

    # New we annotate -- 
    command_line = ["cg_annotate", "--context=100000", "--show-percs=no"]
    command_line.extend(runs)

    annotate_file_name = os.path.join(temporary_dir, "annotation")
    with open(annotate_file_name, "wb+") as f:
        complete_annotation = subprocess.run(command_line, stdout=f, stderr=subprocess.PIPE)
    try: 
        complete_annotation.check_returncode()
    except subprocess.CalledProcessError:
        print("cdof: Somehow cachegrind annotate seems to have failed")
        print(cachegrind_output.stderr)
        shutil.rmtree(temporary_dir)
        exit(1)

    # We also need to run objdump on it
    command_line = ["objdump", "-dS", bin_path]
    objdump_file_name = os.path.join(temporary_dir, "dump")
    with open(objdump_file_name, "wb+") as f:
        subprocess.run(command_line, stdout=f, check=True)

    print("cdof: Adding the prefetch instructions") 
    handle_logic(cachegrind=annotate_file_name, objdump=objdump_file_name, ddisasm=args.ddisasm)

    # Now we need to reassamble it
    with_prefetch_asm = args.ddisasm + "with_prefetch.s"
    with_prefetch_bin_name = bin_name + "with_prefetch"
    
    print("cdof: Reassambling")
    command_line = ["gcc", "-nostartfiles", with_prefetch_asm, "-o", with_prefetch_bin_name]
    subprocess.run(command_line, check=True)
    shutil.rmtree(temporary_dir)
