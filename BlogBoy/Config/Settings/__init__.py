import logging
import os

log_format = ' '.join([
    '[%(asctime)s]',
    '[%(process)d-%(thread)d]',
    '%(levelname)s',
    '-',
    '%(message)s'
])


def get_config(env):
    return '.'.join(['Config', 'Settings',
                     env, 'Config'])


formatter = logging.Formatter(log_format)

def setup_config_logger(app):
    env = os.environ.get('ENV', 'dev')
    config = get_config(env)
    app.config.from_object(config)
    # logHandler = logging.FileHandler('/var/log/blogboy/app-stderr.log')
    # logHandler.setFormatter(formatter)
    # app.logger.addHandler(logHandler)
    # app.logger.setLevel(logging.DEBUG)
