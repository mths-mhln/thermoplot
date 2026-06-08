import os
import sys
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')

import matplotlib.pyplot as plt
from src.thermoplot import thermoplot


input_file_path = "config/R1234ze(E).ini"
fig = thermoplot(input_file_path)
plt.show()

