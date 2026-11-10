import os
import sys
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')

import matplotlib.pyplot as plt
from src.thermoplot import thermoplot_cached

fig = thermoplot_cached(thermoplot_config_file_path="config/CO2.ini")
axes = fig.get_axes()
plt.show()