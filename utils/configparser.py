import configparser


class Config:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self.config_parser = configparser.ConfigParser()
        self.config_parser.optionxform = str  # Preserve case sensitivity of keys
        self.config_parser.read(config_file)
    
    def _parse_value(self, value: str) -> float | str | bool | list:
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            return [self._parse_value(item) for item in value[1:-1].split(",")]
        elif value.lower() in ["true", "false"]:
            return value.lower() == "true"
        else:
            try:
                return float(value)
            except ValueError:
                return value

    def get_thermoplot_settings(self) -> dict[str, float]:
        necessary_thermoplot_settings = [
            "fluid_name",
            "show_spinodal",
            "show_isolines",
            "show_critical_point",
            "show_critical_isobar",
            "s_range",
            "T_range"
        ]
        if not all(req in self.config_parser.options("THERMOPLOT SETTINGS") for req in necessary_thermoplot_settings):
            missing_reqs = [req for req in necessary_thermoplot_settings if req not in self.config_parser.options("THERMOPLOT SETTINGS")]
            raise ValueError(f"Missing necessary thermoplot settings in config file: {missing_reqs}")
        self.thermoplot_settings = {key: self._parse_value(value) for key, value in self.config_parser.items("THERMOPLOT SETTINGS")}

        