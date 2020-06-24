import yaml


def read_yaml(file_name):
    with open(file_name, mode='r', encoding='utf8') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
        return config


def write_yaml(data, file_name):
    with open(file_name, mode='a', encoding='utf8') as file:
        config = yaml.dump(data, file)
        return config
