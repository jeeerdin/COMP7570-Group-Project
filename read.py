from Address import Address
from Transaction import Transaction

YEAR = 2009
DATA_PATH = "./data/edges{}/".format(YEAR)

# dictionary which maps each transaction hash to a pointer to its associated Transaction object
transactions = {}
# dictionary which maps each address hash to a pointer to its associated Address object
addresses = {}

# Stores transaction data as Hash : (time,inputs,output)
tx_data = {}

input_files = [DATA_PATH + "inputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]
output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

def parse_input_line(input_line):

  # Remove end of line
  input_line = input_line[:-1]

  # Split by tab
  input_line = input_line.split('\t')

  # Parse time
  input_line[0] = int(input_line[0])

  # Parse transaction hash
  input_line[1] = hex(int(input_line[1],16))

  for i in range(2,len(input_line),2):
    # Parse the first input's transaction hash
    input_line[i] = hex(int(input_line[i],16))
    
    # Parse the first input's index
    input_line[i+1] = int(input_line[i+1])
  
  return input_line

def parse_output_line(output_line):

  # Remove end of line
  output_line = output_line[:-1]

  # Split by tab
  output_line = output_line.split('\t')

  # Parse time
  output_line[0] = int(output_line[0])

  # Parse transaction hash
  output_line[1] = hex(int(output_line[1],16))

  for i in range(2,len(output_line),2):
    # Parse the first output's address
    output_line[i] = output_line[i]
  
    # Parse the first output's amount
    output_line[i+1] = int(output_line[i+1])

  return output_line

def read_input_file(i):
    file_object = open(input_files[i], "r")

    for input_line in file_object:
      l = parse_input_line(input_line)
      time = l[0]
      hashh = l[1]
      inputs = l[2:]
      pretty_inputs = []
      for i in range(0,len(inputs),2):
          pretty_inputs.append({'Transaction Hash':inputs[i],
                                'Output Index':inputs[i+1],
                                'Address':None,
                                'Amount':None})
      tx_data[hashh] = {'Time':time,'Inputs':pretty_inputs,'Outputs':None}

    file_object.close()

def read_output_file(i):
    file_object = open(output_files[i], "r")

    for output_line in file_object:
      l = parse_output_line(output_line)
      hashh = l[1]
      outputs = l[2:]
      pretty_outputs = []
      for i in range(0,len(outputs),2):
          pretty_outputs.append({'Address':outputs[i],
                                'Amount':outputs[i+1]})
      tx_data[hashh]['Outputs'] = pretty_outputs

    file_object.close()


def read_all_input():
  for i in range(12):
    read_input_file(i)  

def read_all_output():
  for i in range(12):
    read_output_file(i)

read_all_input()
read_all_output()

# TODO: in the transactions dictionary, the address and amount of the inputs are None. This needs to be filled up I think this is "linking the inputs and outputs

# iterating through transaction creating Transaction objects and adding them to the graph as we go
for tx in tx_data.items():

  hashh = tx[0]
  transaction_data = tx_data[hashh]

  # instantiates the object
  tx_obj = Transaction(hashh, transaction_data['Time'])

  # links transaction to all connected outputs
  for addr in transaction_data['Outputs']:

    addr_hash = addr['Address']
    
    # if this is a new address that we have not seen before, we instantiate a new Address object
    if addr_hash not in addresses:
      new_addr = Address(addr_hash)
      addresses[addr_hash] = new_addr

    # transaction appends the address to its list of outputs
    tx_obj.outputs.append(addresses[addr_hash])

    # address appends the transaction to its list of earning_transaction, along with the amount earned
    addresses[addr_hash].earning_transactions.append((tx_obj, addr['Amount']))

    # finally we store the pointer to this new Transaction object in transactions dictionary
    transactions[hashh] = tx_obj
    
# iterating through all transactions again which should now already hae the linked outputs
for tx in tx_data.items():

  hashh = tx[0]

  # getting the transaction object which our output serves as input for
  # this object will currently have an empty inputs list
  tx_obj = transactions[hashh]

  # getting information regarding this transaction from the parsed data
  transaction_data = tx_data[hashh]

  # for each transaction we iterate thrrough each of its inputs
  for input in transaction_data['Inputs']:

    # we get the prev tx and the output index of this input
    prev_tx_hash = input['Transaction Hash']
    output_index = input['Output Index']

    # in the case that the transaction which produced this output comes from an earlier year
    if prev_tx_hash not in transactions:
      addr_obj = Address("{}:{}".format(prev_tx_hash, output_index))

      # adds the Address object to this transactions list of inputs
      tx_obj.inputs.append(addr_obj)

      # we immediately add the transaction with 0 as the amount since we do not know the amount within this input
      addr_obj.spending_transactions.append((tx_obj, 0))

    # otherwise, we know that this address is the output of a transaction that occured in our data's year
    # meaning the address object already exists and can be found at the output index of the previous transaction
    else:
      addr_obj = transactions[prev_tx_hash].outputs[output_index]

      # adds the Address object to this transactions list of inputs
      tx_obj.inputs.append(addr_obj)
    
      spend_tx = (tx_obj, )

      # iterate through the earning transactions ntil we find the correct transaction hash
      for earn_tx in addr_obj.earning_transactions:
        # the 0'th index being the hash of the earning transaction
        if earn_tx[0] == tx_obj.hash:

          # we attach the amount to this pair, so now the spend_tx will look like ( tx_obj, amount )
          spend_tx[1] = earn_tx[1]
          break

      # appending the pair earn_tx to the addresses list of spending_transactions
      addr_obj.spending_transactions.append(spend_tx)

    