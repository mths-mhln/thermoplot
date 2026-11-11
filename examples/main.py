import matplotlib.pyplot as plt
from thermoplot import thermoplot_cached

# This is a T-S diagram for CO2
fig = thermoplot_cached(thermoplot_config_file_path="config/CO2_TS.ini")
plt.show()

# this is a p-h diagram for CO2
fig = thermoplot_cached(thermoplot_config_file_path="config/CO2_PH.ini")
plt.show()

# this is a T-S diagram for R1234ze(E)
fig = thermoplot_cached(thermoplot_config_file_path="config/R1234ze(E)_TS.ini")
plt.show()

# this is a p-h diagram for R1234ze(E)
fig = thermoplot_cached(thermoplot_config_file_path="config/R1234ze(E)_PH.ini")
plt.show()



# this is a p-h diagram for CO2 with some settings overwritten 
# (zoom in, hide isolines and critical point)
thermoplot_overwrite_settings = {
    "show_isolines": False,
    "show_critical_point": False,
    "show_critical_isoline": False,
    "P_range": [6e6, 1e7],
    "H_range": [300e3, 380e3],
}
fig = thermoplot_cached(thermoplot_config_file_path="config/CO2_PH.ini", thermoplot_overwrite_settings=thermoplot_overwrite_settings)
plt.show()



# this is a T-S diagram with something drawn on top
fig = thermoplot_cached(thermoplot_config_file_path="config/CO2_TS.ini")
axes = fig.get_axes()
# draw a line from (S=1000, T=250) to (S=2000, T=300)
axes[0].plot([1000, 2000], [250, 300], color='red', lw=2.0, ls='--', zorder=4)
plt.show()

