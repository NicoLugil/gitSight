import yaml

def get_config(filename):
    print(filename)
    with open(filename, 'r') as f:
        c=yaml.safe_load(f)
    return c