import pathlib
import os
import platform

from dotenv import load_dotenv

load_dotenv()
os_sys = platform.system()

PYTHONPATH = pathlib.Path(str(os.getenv("PYTHONPATH")))

if os_sys == 'Windows':
    print(os_sys)
    python_path = pathlib.Path(str(PYTHONPATH).split(';')[0])
    absolut_python_path = python_path.absolute()
    print('PYTHONPATH=' + str(python_path))
elif os_sys == 'Linux':
    print(os_sys)
    python_path = pathlib.Path(str(PYTHONPATH).split(':')[0])
    absolut_python_path = python_path.absolute()
    print('PYTHONPATH=' + str(python_path))

host = str(os.getenv("HOST"))
user = str(os.getenv("DB_USER"))
password = str(os.getenv("PASSWORD"))
db_name = str(os.getenv("DB_NAME"))
port = str(os.getenv("PORT"))

tg_token = str(os.getenv("BOT_TOKEN"))
admins_id = str(os.getenv('BOT_ADMINS'))
