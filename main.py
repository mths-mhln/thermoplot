from utils.configparser import Config
import matplotlib.pyplot as plt
from src.thermoplot import thermoplot


input_file_path = "config/R1234ze(E).ini"
config = Config(config_file=input_file_path)
config.get_thermoplot_settings()

fig = thermoplot(config)
plt.show()

