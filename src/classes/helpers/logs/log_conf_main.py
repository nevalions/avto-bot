# from config import LOG_DIR
#
log_path_filename = f'logs/{__name__}.log'
#
# print(log_path_filename)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'level': 'INFO',
            'filename': log_path_filename,
            'mode': 'w',
            'class': 'logging.FileHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_handler'],
            'level': 'INFO',
            'propagate': True
        },
    }
}