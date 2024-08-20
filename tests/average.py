import numpy as np
import os
import subprocess
import argparse
import math
from pathlib import Path
from tqdm import tqdm

def collect_stats(file_name, test_args, sample_n):    
    print(f"Running: {file_name} {test_args}")
    
    
    open("output.txt", 'w')
    
    max_llc_missrate = -1
    max_miss_rate = -1
    avg_miss_rate = 0
    avg_llc_missrate = 0
    total_time = 0
    
    for _ in range(sample_n):
        has_nan = True
        samples = None

        # Keep measuring until perf doesn't return nan        
        while (has_nan):
            cmd_line = f"perf stat -o ./output.txt -I 1 -r 3 -x __ -e cache-references,cache-misses,LLC-loads,LLC-load-misses {file_name} {test_args}"
            subprocess.run(cmd_line, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            file_path = Path(file_name).parent / "output.txt"
            samples = np.genfromtxt(file_path, delimiter='__')  
            has_nan = any([math.isnan(x) for x in samples.T[0:2].flatten()])
                    
        time, count = samples.T[0:2]
        
        cache_references = count[0]
        cache_misses = count[1]
        LLC_loads = count[2]
        LLC_load_misses = count[3]
        
        missrate = cache_misses / cache_references
        llc_missrate = LLC_load_misses / LLC_loads
        
        avg_miss_rate += missrate
        avg_llc_missrate += llc_missrate
        total_time += time[-1]
        
        max_llc_missrate = max(llc_missrate, max_llc_missrate)
        max_miss_rate = max(missrate, max_miss_rate)
    
    os.remove("./output.txt")

    avg_miss_rate = (avg_miss_rate / sample_n) * 100
    avg_llc_missrate = (avg_llc_missrate / sample_n) * 100
    avg_time = total_time / sample_n

    return max_llc_missrate * 100, max_miss_rate * 100, avg_miss_rate, avg_llc_missrate, avg_time

def get_args_array(test_csv):
    file_path = Path(test_csv).parent / test_csv
    samples = np.genfromtxt(file_path, delimiter=" ", skip_header=1)
    return samples

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument("test_name", type=str) 
    parser.add_argument("test_csv", type=str)
    parser.add_argument("samples", type=int) 
    args = parser.parse_args()
    
    os.makedirs("{}_measurements".format(args.test_name),exist_ok=True)
    
    noprefetch = f"./{args.test_name}.o"
    prefetch = f"./{args.test_name}.owith_prefetch"
    test_args_array = get_args_array(args.test_csv)
    results = {
        'max_llc_missrate': [],
        'max_miss_rate': [],
        'avg_miss_rate': [],
        'avg_llc_missrate': [],
        'time': []
    }
    
    for test_args in tqdm(test_args_array):
        if (test_args.size > 1):
            test_args = " ".join(str(x) for x in test_args)

        prefetch_stats = collect_stats(prefetch, test_args, args.samples)
        noprefetch_stats = collect_stats(noprefetch, test_args, args.samples)
    
        for i, key in enumerate(results.keys()):
            results[key].append([prefetch_stats[i], noprefetch_stats[i]])

    # Save Data
    for key, data in results.items():
        filename = f"{args.test_name}_{key}_results.csv"
        path = "{}_measurements/{}".format (args.test_name, filename)    
        np.savetxt(path, np.array(data), delimiter=",", 
                   header="prefetch,noprefetch", comments='')
        print(f"Saved {filename}")


main()