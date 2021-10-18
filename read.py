YEAR = 2015
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


def read_all_input():
  for i in range(12):
    file_object = open(input_files[0], "r")

    for input_line in file_object:
      # TODO: do something with this
      parse_input_line(input_line)

    file_object.close()

def read_all_output():
  for i in range(12):
    file_object = open(output_files[0], "r")

    for output_line in file_object:
      # TODO: do something with this
      parse_output_line(output_line)
      
    file_object.close()
