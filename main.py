from utils.configparser import Config


input_file_path = "config/R1234ze(E).ini"
config = Config(config_file=input_file_path)
config.get_thermoplot_settings()
print(config.thermoplot_settings)

