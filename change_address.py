'''
Reads a numpy array from disk that contains all the addresses in sorted order
It then replaces the addresse in the outputs .txt file with the index into this array
It writes the results to outputs2015_i_eff.txt
'''
import numpy as np
import cProfile

YEAR = 2015
DATA_PATH = "./data/edges{}/".format(YEAR)
    
# load the sorted addresses
addr_dir = np.load('addr_dir.npy')

# A list of all input files
output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

def parse_output_line(output_line):
  '''
  Takes a line from the output files,
  removes its timestamp, and replaces addresses with
  that address's index into the sorted address directory
  '''

  # Store the end of line
  eol = output_line[-1]
  # Remove end of line
  output_line = output_line[:-1]

  # Split by tab
  output_line = output_line.split('\t')

  for i in range(2,len(output_line),2):
    idx = np.searchsorted(addr_dir,output_line[i])
    output_line[i] = str(idx) # replace address into index

  return '\t'.join(output_line) + eol

def read_output_file(i):
    '''
    Reads a output file line by line
    modifies the line to have indeces instead of addresses
    and dumps the line to the end of a new file
    '''
    file_object = open(output_files[i], "r")
    output_file = open(output_files[i][:-4]+'_eff.txt',"a")

    for output_line in file_object:
      parsed_line = parse_output_line(output_line)
      output_file.write(parsed_line)

    file_object.close()
    output_file.close()


def read_all():
    '''
    Reads every output file
    '''
    for i in range(12):
        print(i)
        read_output_file(i)

if __name__ == '__main__':
    cProfile.run('read_all()')
