from configs.config_loader import ConfigReaderInstance
import logging 
import logging.config

class Config:
    """Returns a config instance depending on the ENV_STATE variable."""
    def __init__(self, args=None):
        self.LOGGER = ConfigReaderInstance.yaml.read_config_from_file("settings/logging.yml")
        logging.config.dictConfig(self.LOGGER)

        if args.override_default_config:
            setting_folder = args.override_default_config
        else:
            setting_folder = "settings"

        self.CONF = ConfigReaderInstance.yaml.read_config_from_file(f"{setting_folder}/config.yml")

def set_config(args):
    global settings
    settings = Config(args)
