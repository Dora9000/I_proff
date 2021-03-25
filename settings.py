
from __future__ import print_function
import pathlib
from copy import deepcopy
import yaml

BASE_DIR = pathlib.Path(__file__).parent
CONFIG_PATH = BASE_DIR / 'config' / 'config.yaml'


def get_config(path):
    with open(path) as file:
        config = yaml.full_load(file)
        return config


def get_secure_config(config):
    config = deepcopy(config)
    return config
