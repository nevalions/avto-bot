import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

PYTHONPATH = pathlib.Path(str(os.getenv("PYTHONPATH")))
python_path = pathlib.Path(str(PYTHONPATH).split(';')[0])
absolut_python_path = python_path.absolute()

print(PYTHONPATH)
print(python_path)
print(absolut_python_path)


host = str(os.getenv("HOST"))
user = str(os.getenv("DB_USER"))
password = str(os.getenv("PASSWORD"))
db_name = str(os.getenv("DB_NAME"))
port = int(os.getenv("PORT"))

# logging_config = logs.LOGGING_CONFIG
# autolog_debug = logs.autolog_debug()
# autolog_info = logs.autolog_info()
# autolog_warning = logs.autolog_warning()

# print(SRC_DIR)
# print(SRC_DIR_ABSOLUTE)
# print(ROOT_DIR)
# print(LOG_DIR)
# print(host)
# print(user)
# print(db_name)
# print(port)


