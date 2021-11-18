'''
This file reads all the addresses, sorts them and stores it in a numpy array
'''
import gc
import numpy as np
import cProfile

YEAR = 2015
DATA_PATH = "../data/edges/edges{}/".format(YEAR)
    
# A set containing all known addresses
addr_dir = {'prevyear','noaddress'}

# A list of output files
output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]


def parse_output_line(output_line):
  '''
  Takes a line from the output file and adds all addresses
  present to the address directory
  '''
  # Remove end of line
  output_line = output_line[:-1]

  # Split by tab
  output_line = output_line.split('\t')
  for i in range(2,len(output_line),2):
    addr_dir.add(output_line[i])

def read_output_file(i):
    '''
    Reads each line of an output file 
    and parses it
    '''
    file_object = open(output_files[i], "r")

    for output_line in file_object:
      parse_output_line(output_line)

    file_object.close()

def read_all():
    '''
    Reads every output file
    '''
    global addr_dir
    for i in range(12):
        print("Output File Number: {}".format(i))
        read_output_file(i)
    addr_dir = list(addr_dir)
    gc.collect()
    addr_dir.sort()
    gc.collect()
    np.save('addr_dir.npy',addr_dir)

if __name__ == '__main__':
    cProfile.run("read_all()")
