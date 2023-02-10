import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

SRC_DIR = pathlib.Path(str(os.getenv("SRC_DIR")))
SRC_DIR_ABSOLUTE = pathlib.Path.absolute(SRC_DIR)
ROOT_DIR = pathlib.Path.absolute(SRC_DIR).parents[0]
LOG_DIR = SRC_DIR_ABSOLUTE / "log_dir"

host = str(os.getenv("HOST"))
user = str(os.getenv("DB_USER"))
password = str(os.getenv("PASSWORD"))
db_name = str(os.getenv("DB_NAME"))
port = int(os.getenv("PORT"))

# logging_config = log_dir.LOGGING_CONFIG
# autolog_debug = log_dir.autolog_debug()
# autolog_info = log_dir.autolog_info()
# autolog_warning = log_dir.autolog_warning()

# print(SRC_DIR)
# print(SRC_DIR_ABSOLUTE)
# print(ROOT_DIR)
# print(LOG_DIR)
# print(host)
# print(user)
# print(db_name)
# print(port)
