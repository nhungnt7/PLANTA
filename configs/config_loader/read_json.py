import json
from abc import ABC
from pathlib import Path

from configs.config_loader.config_interface import ConfigReaderInterface
from configs.config_loader.serializer import Struct

class JsonConfigReader(ConfigReaderInterface, ABC):

    def __init__(self):
        super(JsonConfigReader, self).__init__()

    def read_config_from_file(self, config_path: str):
        with open(config_path) as file:
            config = json.load(file)
        # config_object = Struct(**config)
        return config
