import logging.config
from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_info, autolog_warning

from datetime import datetime

from src.db import AutoBotTgUsersDB, AutoBotUserDB, AutoBotMainDB, AutoBotAutoDB
from src.classes import User, Car

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

now = datetime.now()


def main():
    autolog_info(f'Main app started')

    db_user = AutoBotUserDB()
    db_auto = AutoBotAutoDB()
    db_main = AutoBotMainDB()
    db_tg_user = AutoBotTgUsersDB()

    car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BLABLABLA', '300000')
    user = User('NEW2', 'asd123qwe@added.ru')

    try:
        print(db_user.search_user_email_in_db('email', 'ASDsa7@added.ru'))
        print(db_tg_user.search_tg_user_chat_id_in_db('chat_id', 84891021))
        print(*vars(car).values())
        add_u = db_user.add_user(*vars(user).values())
        print(f'car id: {db_auto.add_car(*vars(car).values())}')
        print(f'user id: {add_u}')
        #
        db_user.update_user_username('ASDsa7@added.ru', 'Super New')
        #
        # print(*db_auto.get_all_cars_in_db(), sep='\n')
        # print(*db_user.get_all_users_in_db(), sep='\n')
        # print(db_auto.get_car_by_car_id(12))
        # print(db_user.get_user_by_user_id(13))
        #
        # users_cars = db_main.show_all_users_cars(16)
        # print(*users_cars, sep='\n')
        # for car in users_cars:
        #     print(f"{car['model']} {car['model_name']}")
        #
        # db_main.add_car_to_user_in_db(16, 17)

    except Exception as ex:
        print(ex)
    finally:
        db_auto.close()


if __name__ == '__main__':
    main()
