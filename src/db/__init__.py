import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'db'))

from db_user_helper import AutoBotUserDB
from db_auto_helper import AutoBotAutoDB
from db_main_helper import AutoBotMainDB
from db_tg_users import AutoBotTgUsersDB