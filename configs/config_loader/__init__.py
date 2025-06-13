from pydantic.dataclasses import dataclass

from configs.config_loader.read_json import JsonConfigReader
from configs.config_loader.read_yaml import YamlConfigReader

@dataclass
class ConfigReaderInstance:
    json = JsonConfigReader()
    yaml = YamlConfigReader()