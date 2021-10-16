YEAR = 2015
DATA_PATH = "./data/edges{}/".format(YEAR)


input_files = [DATA_PATH + "inputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]
output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

hash_to_hex = lambda h : hex(int(h,16))

def parse_input_line(input_line):

  # Remove end of line
  input_line = input_line[:-2]

  # Split by tab
  input_line = input_line.split('\t')

  line_len = len(input_line) # Remove for efficiency

  # Pares from string to appropiate data type
  parsed_line = []

  # Parse time
  time = input_line.pop(0)
  parsed_line.append(int(time))

  # Parse transaction hash
  t_hash = input_line.pop(0)
  parsed_line.append(hash_to_hex(t_hash))

  for _ in range(len(input_line)//2):
    # Parse the first input's transaction hash
    input_hash = input_line.pop(0)
    parsed_line.append(hash_to_hex(input_hash))
  
    # Parse the first input's index
    input_index = input_line.pop(0)
    parsed_line.append(int(input_index))

  assert len(input_line) == 0 # Remove for efficiency
  assert line_len == len(parsed_line)# Remove for efficiency

  return parsed_line

def parse_output_line(output_line):

  # Remove end of line
  output_line = output_line[:-2]

  # Split by tab
  output_line = output_line.split('\t')

  line_len = len(output_line) # Remove for efficiency

  # Pares from string to appropiate data type
  parsed_line = []

  # Parse time
  time = output_line.pop(0)
  parsed_line.append(int(time))

  # Parse transaction hash
  t_hash = output_line.pop(0)
  parsed_line.append(hash_to_hex(t_hash))

  for _ in range(len(output_line)//2):
    # Parse the first output's address
    output_add = output_line.pop(0)
    parsed_line.append(output_add)
  
    # Parse the first output's amount
    output_amount = output_line.pop(0)
    parsed_line.append(int(output_amount))

  assert len(output_line) == 0 # Remove for efficiency
  assert line_len == len(parsed_line)# Remove for efficiency

  return parsed_line


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
      print(parse_output_line(output_line))
      
    file_object.close()

read_all_input()
read_all_output()
