import scipy
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
import cProfile


YEAR = 2010
DATA_PATH = "./data/edges{}/".format(YEAR)

# Stores transaction data as Hash : (inputs,output)
tx_data = []

# Address and transaction hash look up
addr_dir = {'prevyear':0,'noaddress':1}
tx_dir = {}
num_addr = 2
num_tx = 0

input_files = [DATA_PATH + "inputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]
output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

def parse_output_line(output_line):
  global num_addr,num_tx

  # Remove end of line
  output_line = output_line[:-1]

  # Split by tab
  output_line = output_line.split('\t')

  # Parse transaction hash
  output_line[1] = hex(int(output_line[1],16))
  
  # Add transaction hash to the transaction directory
  # if it is not already in there
  tx_dir[output_line[1]] = num_tx
  num_tx += 1

  outputs = []
  for i in range(2,len(output_line),2):
    # Add address to the address directory
    # if it is not already in there
    try:
      addr_dir[output_line[i]]
    except KeyError:
      addr_dir[output_line[i]] = num_addr
      num_addr += 1
  
    # Parse the first output's amount
    output_line[i+1] = int(output_line[i+1])
    outputs.append((addr_dir[output_line[i]],output_line[i+1]))

  tx_data.append(([],outputs))

def read_output_file(i):
    file_object = open(output_files[i], "r")

    for output_line in file_object:
      parse_output_line(output_line)

    file_object.close()

def read_all_output():
  for i in range(12):
    print(i)
    read_output_file(i)

def parse_input_line(input_line):

  # Remove end of line
  input_line = input_line[:-1]

  # Split by tab
  input_line = input_line.split('\t')

  # Parse transaction hash and convert to id
  input_line[1] = tx_dir[hex(int(input_line[1],16))]

  for i in range(2,len(input_line),2):
    try:
      # Parse the first input's transaction hash and convert to id
      input_line[i] = tx_dir[hex(int(input_line[i],16))]
      
      # Parse the first input's index
      input_line[i+1] = int(input_line[i+1])
    
      output = tx_data[input_line[i]][1][input_line[i+1]]
      tx_data[input_line[1]][0].append(output)
    except KeyError:
      tx_data[input_line[1]][0].append((addr_dir['prevyear'],None))

def read_input_file(i):
    file_object = open(input_files[i], "r")

    for input_line in file_object:
      parse_input_line(input_line)

    file_object.close()

def read_all_input():
  for i in range(12):
    print(i)
    read_input_file(i)

def create_graph():

    addr_to_tx = lil_matrix((num_addr,num_tx),dtype = 'float64')
    tx_to_addr = lil_matrix((num_tx,num_addr),dtype = 'float64')

    for tx_idx in range(num_tx):
        tx = tx_data[tx_idx]
         
        # Link inputs to this transaction
        for inp in tx[0]:
            input_idx = inp[0]
            input_amount = inp[1]
            addr_to_tx[input_idx,tx_idx] = input_amount

        # Link the transaction to its outputs
        for out in tx[1]:
            output_idx = out[0]
            output_amount = out[1]
            tx_to_addr[tx_idx,output_idx] = output_amount
            
    return csr_matrix(addr_to_tx), csr_matrix(tx_to_addr)

cProfile.run('read_all_output()')
cProfile.run('read_all_input()')
#cProfile.run('create_graph()')
addr_to_tx,tx_to_addr = create_graph()
