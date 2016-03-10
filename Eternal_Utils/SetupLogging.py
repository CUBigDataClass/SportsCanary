import os
import json
import logging.config
import logging


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    path = os.getcwd() + '/Eternal_Utils/logging.json'
    print path
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print 'Path doesnt exist'
        logging.basicConfig(level=default_level)

