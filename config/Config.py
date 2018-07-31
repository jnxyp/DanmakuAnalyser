import json
from config.Constants import *


def reload_config(path: str = os.path.join(PROJECT_PATH, 'config', 'config.json')):
    with open(path) as json_file:
        config = json.load(json_file)
    return config


_config = reload_config()  # type:dict


def config(s: str = None):
    '''
    Query specific configuration value.
    :param s: Query string in format "node_name.node_name.value_name".
    :return: configuration value or dictionary.
    '''
    if s is None:
        return _config
    s = s.split('.')
    value = _config
    while len(s) > 0:
        value = value[s.pop(0)]
    return value


if __name__ == '__main__':
    print(config())
    print(config('networks'))
    print(config('networks.max_threads'))
