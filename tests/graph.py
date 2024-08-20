# Title: measure.py
# Description: Generates a graph comparing cache miss rates of CDOF optimized 
# and unoptimized C programs.

import matplotlib.pyplot as plt
import numpy as np
import re
import os, fnmatch
import argparse

from pathlib import Path

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def gen_graph (file_path):
  # Extract Sample data
  samples   = np.genfromtxt(file_path, delimiter=",", skip_header=1)
  op, nop   = samples.T
  
  
  match = re.search(r'test_(.*?)_results\.csv', os.path.basename(file_path))
  labely =match.group(1)
  
  x = np.arange (0, op.size)  
  
  plt.figure(figsize=(10,6))
  plt.title(file_path)
  
  plt.plot(x, op, label='Optimized')
  plt.plot(x, nop, label='Unoptimized')
  plt.ylabel(labely)
  plt.xlabel("Input Size")
  # Set x-axis to be discrete
  
  plt.xticks(x)
  
  # Set y-axis limits
  y_min = min(op.min(), nop.min()) * 0.9
  y_max = max(op.max(), nop.max()) * 1.1
  plt.ylim(y_min, y_max)
  
  # plt.yscale('log')
  
  plt.legend()
  plt.tight_layout()
  plt.savefig ("{}.png".format(file_path))



def main ():
  # Get Target csv 
  parser = argparse.ArgumentParser ()  
  parser.add_argument ("test_name", help="csv to graph", type=str) 
  args = parser.parse_args ()
  dir_name = "{}_measurements".format(args.test_name)
  
  csv_list = find('*_results.csv', dir_name)
  
  for csv in csv_list:
    gen_graph (csv)
  
  


main ()
