The results for this step are stored in a matrix which includes equal portions or darknet address and regular addresses. For each address, a number of features are stored, these features are described below.

Address Features:
- Sum of input amounts
- Sum of output amounts
- Number of inputs received
- Number of outputs spent
- Average input amount
- Average output amount
- Standard deviation of input amounts
- Standard deviation of input amounts
- Ratio of number of inputs to outputs

Since there are frequently cases where the amount of a darknet transaction can be associated with multiple outputs. We also assign each address with a confidence level.

A confidence level of 0 would suggest the address is definitely not on the 2014 list of darknet transactions.
A confidence level of 1 suggest the address is a guaranteed match to one of the darknet transactions.
The address is only included if the confidence is at least 50%

To avoid bias based on greater density of transactions from any given part of the year, the darknet transactions list was scrambled prior to the matching process.
