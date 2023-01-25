from datetime import datetime

from db_user_helper import AutoBotUserDB
from db_auto_helper import AutoBotAutoDB
from db_main_helper import AutoBotMainDB
from users import User
from cars import Car

now = datetime.now()


def main():
    db_user = AutoBotUserDB()
    db_auto = AutoBotAutoDB()
    db_main = AutoBotMainDB()

    car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023')
    user = User('NEW2', 'ASDsa7@added.ru')

    try:

        add_u = db_user.add_user(*vars(user).values())
        print(f'car id: {db_auto.add_car(*vars(car).values())}')
        print(f'user id: {add_u}')

        db_user.update_user_username('ASDsa7@added.ru', 'Super New')

        print(*db_auto.get_all_cars_in_db(), sep='\n')
        print(*db_user.get_all_users_in_db(), sep='\n')
        print(db_auto.get_car_by_car_id(12))
        print(db_user.get_user_by_user_id(13))

        users_cars = db_main.show_all_users_cars(15)
        print(*users_cars, sep='\n')
        for car in users_cars:
            print(f"{car['model']} {car['model_name']}")

        db_main.add_car_to_user_in_db(16, 17)

    except Exception as ex:
        print(ex)
    finally:
        db_auto.close()


def create_user():
    """
    Create user with terminal.
    :return:
    """
    try:
        return User(input('Enter your name: '), input('Enter your email: '))
    except Exception as ex:
        print('User is not created!')
        raise ex


def create_car():
    """
    Create car with terminal.
    :return:
    """
    try:
        new_car = Car(
            input('Enter car model: '),
            input('Enter car model name: '),
            input('Enter car mileage: '),
            input('Enter mileage measures (km or miles): '),
            f'{now.strftime("%d.%m.%Y")}',

            input('Enter car description (optional): '),
        )
        print(f'Car {new_car.model} {new_car.model_name} created')
        return new_car
    except Exception as ex:
        print('Car is not created!')
        raise ex


if __name__ == '__main__':
    main()
