import csv
import os
import sys
from typing import Dict
from typing import Any
from urllib.parse import urlparse
from pathlib import Path

class ConfigError(Exception):
    pass 

class PackageManager:
    def __init__(self):
        self.config = {}
        self.required_params = ['package_name', 'repository_yrl', 'test_repo_mode', 'ascii_tree_output', 'max_depth']

    def load_config(self, config_path: str) -> Dict[str, Any]:
        if not os.path.exists(config_path):
            raise ConfigError("Конфигурационный файл не найден: {config_path}")
        config ={}
        try:
            with open(config_path, 'r', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    param = row['parametr'].strip()
                    value = row['value'].strip()
                    config[param] = value
        except csv.Error as e:
            raise ConfigError("Ошибка чтения CSV файла: {e}")
        except KeyError as e:
            raise ConfigError("Ошибка чтения CSV файла: {e}")
        except Exception as e:
            raise ConfigError("Ошибка чтения CSV файла: {e}")

        missing_params = [param for param in self.required_params if param not in config]
        if(missing_params):
            raise ConfigError(f"Ошибка чтения CSV файла: {', '.join(missing_params)}")
        validated_config = self._validate_config(config)
        return validated_config