import os
import json
import logging.config
import logging


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Loads logging setup file.
    :param default_path: If no path is given uses default
    :param default_level: Default level is info if no other is set
    :param env_key: Allows for setting Config from the enviorment
    """
    value = os.getenv(env_key, None)
    path = os.getcwd() + '/Eternal_Utils/logging.json'
    if value:  # pragma: no cover
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        return True
    else:  # pragma: no cover
        print 'Path doesnt exist'
        logging.basicConfig(level=default_level)
        return False
