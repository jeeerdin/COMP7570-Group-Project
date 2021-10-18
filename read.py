import threading

YEAR = 2010
DATA_PATH = "./data/edges{}/".format(YEAR)

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


# Stores a transaction as Hash : (time,inputs,output)
transactions = {}

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
      transactions[hashh] = {'Time':time,'Inputs':pretty_inputs,'Outputs':None}

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
      transactions[hashh]['Outputs'] = pretty_outputs

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
