# -*- coding: utf-8 -*-
import os

def get_config_env():
    config = {
        'TABLE_NAME_MESSAGE': os.getenv('TABLE_NAME_MESSAGE'),
    }
    return config