import numpy as np
import scipy as sc
from scipy import sparse as sp
import datetime as dt

tx_to_addr = sp.load_npz("months_1_to_12_btc_transactions_tx_to_addr.npz").astype('uint64')
addr_to_tx = sp.load_npz("months_1_to_12_btc_transactions_addr_to_tx.npz").astype('uint64')

time_convert = lambda x: dt.datetime.utcfromtimestamp(x).strftime("%Y/%m/%d %H:%M")


YEAR = 2015
DATA_PATH = "./data/edges{}/".format(YEAR)
    
output_files = [DATA_PATH + "outputs{}_{}_tx.txt".format(YEAR,i) for i in range(1,13)]

num_days = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
# a dictionary with the day as the key and a list of tID's at that day
daily_index = {} 


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

  timestamp = time_convert(int(output_line[0]))
  tId = int(output_line[1])

  day = int(timestamp[8:10])
  daily_index[day].append(tId)

def read_output_file(i):
    '''
    Reads a output file line by line
    modifies the line to have indeces instead of transaction hashes
    and dumps the line to the end of a new file
    '''

    global daily_index
    # initilize the dictionary
    days = num_days[i+1]
    daily_index = {}
    for j in range(1,days+1):
        daily_index[j] = []

    file_object = open(output_files[i], "r")

    for output_line in file_object:
      parse_output_line(output_line)

    file_object.close()

    for j in range(1,days + 1):
        day_idx = daily_index[j]
        day_addr_to_tx = addr_to_tx[:,day_idx]
        day_tx_to_addr = tx_to_addr[day_idx,:]
        sp.save_npz("daily_graphs/{}_{}_addr_to_tx.npz".format(i+1,j),day_addr_to_tx)
        sp.save_npz("daily_graphs/{}_{}_tx_to_addr.npz".format(i+1,j),day_tx_to_addr)

def read_all():
    '''
    Reads every output and input file
    '''
    for i in range(12):
        print(i)
        read_output_file(i)


read_all()
