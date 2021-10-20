import scipy
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
import cProfile
import gc
from bidict import bidict

YEAR = 2015
DATA_PATH = "./data/edges{}/".format(YEAR)
MAX_NUM_ADDR = int(75000000)
MAX_NUM_TX = int(50000000)
    
addr_to_tx = csr_matrix((MAX_NUM_ADDR,MAX_NUM_TX),dtype = 'float64')
tx_to_addr = csr_matrix((MAX_NUM_TX,MAX_NUM_ADDR),dtype = 'float64')

# Stores transaction data as Hash : (inputs,output)
tx_data = {}

# Address and transaction hash look up
addr_dir = {'prevyear':0,'noaddress':1}
tx_dir = bidict({})
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
    outputs.append([addr_dir[output_line[i]],output_line[i+1],False])

  tx_data[num_tx] = [[],outputs]
  num_tx += 1

def read_output_file(i):
    file_object = open(output_files[i], "r")

    for output_line in file_object:
      parse_output_line(output_line)

    file_object.close()

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
      tx_data[input_line[i]][1][input_line[i+1]][2] = True
      tx_data[input_line[1]][0].append([output[0],output[1]])
    except KeyError:
      tx_data[input_line[1]][0].append([addr_dir['prevyear'],None])

def read_input_file(i):
    file_object = open(input_files[i], "r")

    for input_line in file_object:
      parse_input_line(input_line)

    file_object.close()

def create_graph():

    to_delete = []
    tx_to_addr_update = [[],[],[]]
    addr_to_tx_update = [[],[],[]]
    for tx_idx in tx_data.keys():       
        tx = tx_data[tx_idx]
         
        # Link inputs to this transaction if it has not been linked
        if tx[0] != None:
          for inp in tx[0]:
              input_idx = inp[0]
              input_amount = inp[1]
              addr_to_tx_update[0].append(input_idx)
              addr_to_tx_update[1].append(tx_idx)
              addr_to_tx_update[2].append(input_amount)

        # Once the inputs are linked We can delete the inputs
        # As they are no longer needed
        tx_data[tx_idx][0] = None

        # Link the transaction to its outputs
        deleteable = True
        for out in tx[1]:
            output_idx = out[0]
            output_amount = out[1]
            deleteable = deleteable and out[2]
            tx_to_addr_update[0].append(tx_idx)
            tx_to_addr_update[1].append(output_idx)
            tx_to_addr_update[2].append(output_amount)
            
        if deleteable:
            to_delete.append(tx_idx)
            del tx_dir.inverse[tx_idx]
            tx_data[tx_idx] = None

    for idx in to_delete:
        del tx_data[idx]
    
    addr_to_tx[addr_to_tx_update[0],addr_to_tx_update[1]] = addr_to_tx_update[2]
    tx_to_addr[tx_to_addr_update[0],tx_to_addr_update[1]] = tx_to_addr_update[2]



def read_one_month(i):
    read_output_file(i)
    print("output {}".format(i))
    read_input_file(i)
    print("input {}".format(i))

    print("Number of transactions in the tx_dir before linking: {}".format(len(tx_dir)))
    create_graph()
    print("Number of transactions in the tx_dir after linking: {}".format(len(tx_dir)))
    gc.collect()
    print()

def read_all():
    for i in range(12):
        read_one_month(i)

cProfile.run('read_all()')
