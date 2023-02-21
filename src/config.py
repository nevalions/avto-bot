import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

PYTHONPATH = pathlib.Path(str(os.getenv("PYTHONPATH")))
python_path = pathlib.Path(str(PYTHONPATH).split(';')[0])
absolut_python_path = python_path.absolute()


host = str(os.getenv("HOST"))
user = str(os.getenv("DB_USER"))
password = str(os.getenv("PASSWORD"))
db_name = str(os.getenv("DB_NAME"))
port = int(os.getenv("PORT"))

tg_token = str(os.getenv("BOT_TOKEN"))
admins_id = str(os.getenv('BOT_ADMINS'))

# print(SRC_DIR)
# print(SRC_DIR_ABSOLUTE)
# print(ROOT_DIR)
# print(LOG_DIR)
# print(host)
# print(user)
# print(db_name)
# print(port)


