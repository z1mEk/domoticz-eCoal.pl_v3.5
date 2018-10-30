import sys
from eSterownik35 import eSterownik35

eStr35 = eSterownik35(IP='192.168.1.50', port='80')

device = int(sys.argv[1])
value = sys.argv[2]

print(eStr35.GetValue(device, value))