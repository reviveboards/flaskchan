import json
import random

def load_config(cfg_file):
    config_file = open(cfg_file)
    cfg = json.load(config_file)
    config_file.close()

    return cfg

def random_motd(cfg):
    random.shuffle(cfg['motd'])
    motd = random.choice(cfg['motd'])

    return motd