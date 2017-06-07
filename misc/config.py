import shutil
import hashlib
import json
import os

from  generic.misc.logger import create_logger

def load_config(config_file, exp_dir):
    with open(config_file, 'rb') as f_config:
        config_str = f_config.read()
        exp_identifier = hashlib.md5(config_str).hexdigest()
        config = json.loads(config_str.decode('utf-8'))

    save_path = '{}/{{}}'.format(os.path.join(exp_dir, exp_identifier))
    if not os.path.isdir(save_path.format('')):
        os.makedirs(save_path.format(''))

    # create logger
    logger = create_logger(save_path.format('train.log'))
    logger.info("Config Hash {}".format(exp_identifier))
    logger.info(config)

    # set seed
    set_seed(config)

    # copy config file
    shutil.copy(config_file, save_path.format('config.json'))

    return config, exp_identifier, save_path

def set_seed(config):
    import numpy as np
    import tensorflow as tf
    seed = config["seed"]
    if seed > -1:
        np.random.seed(seed)
        tf.set_random_seed(seed)