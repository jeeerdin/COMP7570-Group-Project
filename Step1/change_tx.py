'''
This file maintains a dictionary with the transaction hash as a key
and a integer as a value
It then replaces all transaction hashes in the input and output files
and replaces them with this integer
It then writes the result to a file named outputs2015_i_tx.txt and inputs2015_i_tx.txt
'''
import numpy as np
import cProfile

YEAR = 2015
DATA_PATH = "../data/edges/edges{}/".format(YEAR)
    
# A dictionary storing the index asscociated with each transaction
tx_dir = {}
num_tx = 0

output_files = [DATA_PATH + "outputs{}_{}_eff.txt".format(YEAR,i) for i in range(1,13)]
input_files = [DATA_PATH + "inputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

def parse_output_line(output_line):
  '''
  Reads a line from a output file
  and replaces each transaction hash with an index
  '''

  global num_tx

  eol = output_line[-1]
  # Remove end of line
  output_line = output_line[:-1]

  # Split by tab
  output_line = output_line.split('\t')

  tx_dir[output_line[1]] = num_tx
  output_line[1] = str(num_tx)
  num_tx += 1

  return '\t'.join(output_line) + eol

def parse_input_line(input_line):
  '''
  Reads a line from a input file
  and replaces each transaction hash with an index
  '''
  global num_tx

  eol = input_line[-1]
  # Remove end of line
  input_line = input_line[:-1]

  # Split by tab
  input_line = input_line.split('\t')

  # Parse transaction hash and convert to id
  input_line[1] = str(tx_dir[input_line[1]])

  for i in range(2,len(input_line),2):
      if not input_line[i] in tx_dir:
          input_line[i] = 'prevyear'
      else:
          input_line[i] = str(tx_dir[input_line[i]])


  return '\t'.join(input_line) + eol

def read_output_file(i):
    '''
    Reads a output file line by line
    modifies the line to have indeces instead of transaction hashes
    and dumps the line to the end of a new file
    '''
    file_object = open(output_files[i], "r")
    output_file = open(output_files[i][:-8]+'_tx.txt',"a")

    for output_line in file_object:
      parsed_line = parse_output_line(output_line)
      output_file.write(parsed_line)

    file_object.close()
    output_file.close()

def read_input_file(i):
    '''
    Reads a input file line by line
    modifies the line to have indeces instead of transaction hashes
    and dumps the line to the end of a new file
    '''
    file_object = open(input_files[i], "r")
    output_file = open(input_files[i][:-4]+'_tx.txt',"a")

    for input_line in file_object:
      parsed_line = parse_input_line(input_line)
      output_file.write(parsed_line)

    file_object.close()
    output_file.close()


def read_all():
    '''
    Reads every output and input file
    '''
    for i in range(12):
        print(i)
        read_output_file(i)
        read_input_file(i)

if __name__ == '__main__':
    cProfile.run('read_all()')
