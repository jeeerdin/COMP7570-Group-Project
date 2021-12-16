# Our transactions are sorted based on time.
# However, this is not enough information to figure out which day a transaction occured
# We will create a dictionary that maps from tx_id to the day of the year

import numpy as np
import cProfile
from datetime import datetime
from calendar import monthrange

MONTHS = 12
TOTAL_DAYS = 365
YEAR = 2015
DATA_PATH = "../data/edges/edges{}/".format(YEAR)

days_per_month = [0]
for i in range(1,MONTHS):
    days_per_month.append(monthrange(YEAR, i)[1])
days_per_month = np.cumsum(days_per_month)


def get_day(timestamp):
    ts = int(timestamp)
    day = int(datetime.utcfromtimestamp(ts).strftime('%d'))
    month = int(datetime.utcfromtimestamp(ts).strftime('%m'))
    
    return days_per_month[month-1] + day


# A dictionary storing the index asscociated with each transaction
tx_dir = {}
num_tx = 0

output_files = [DATA_PATH + "outputs{}_{}.txt".format(YEAR,i) for i in range(1,13)]

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

  tx_dir[num_tx] = get_day(output_line[0])
  num_tx += 1


def read_output_file(i):
    '''
    Reads a output file line by line
    modifies the line to have indeces instead of transaction hashes
    and dumps the line to the end of a new file
    '''
    file_object = open(output_files[i], "r")

    for output_line in file_object:
      parsed_line = parse_output_line(output_line)

    file_object.close()

def read_all():
    '''
    Reads every output and input file
    '''
    for i in range(MONTHS):
        print(i)
        read_output_file(i)

read_all()


judah = np.load('../data/grams/linked/judah_bad_tId.npy')[:,0]
jordan = np.load('../data/grams/linked/jordan_bad_tId.npy')[:,0]
abram = np.load('../data/grams/linked/abram_bad_tId.npy')[:,0]
tId = np.concatenate([judah,jordan,abram])

days = np.zeros_like(tId)
i = 0

# Now we break the darknet addresses id's into 365 days
for tx in tId:
    days[i] = tx_dir[tx]
    i+=1


for i in range(TOTAL_DAYS):
    print(i)
    np.save('../data/grams/linked/daily_bad_tId/{}.npy'.format(i),tId[days == i])

