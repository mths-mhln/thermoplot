import matplotlib.pyplot as plt
from thermoplot import thermoplot_cached

fig = thermoplot_cached(thermoplot_config_file_path="config/CO2.ini")
plt.show()