import pathlib

SRC_DIR = pathlib.Path('')
SRC_DIR_ABSOLUTE = pathlib.Path.absolute(SRC_DIR)
ROOT_DIR = pathlib.Path.absolute(SRC_DIR).parents[0]

host = '127.0.0.1'
user = 'avto'
password = 'kicker'
db_name = 'avto-bot'
port = 5432
