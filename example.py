import sys
from eSterownik35 import eSterownik35

eStr35 = eSterownik35(IP='87.251.234.136', port='10121')

device = int(sys.argv[1])
value = sys.argv[2]

print(eStr35.GetValue(device, value))