from datetime import datetime

from db_user_helper import AutoBotUserDB
from db_auto_helper import AutoBotAutoDB
from users import User
from cars import Car

now = datetime.now()


def main():
    db_user = AutoBotUserDB()
    db_auto = AutoBotAutoDB()

    car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023')
    user = User('NEW2', 'baaa12sd1235467@added.ru')

    try:

        add_u = db_user.add_user(*vars(user).values())
        print(f'car id: {db_auto.add_car(*vars(car).values())}')
        print(f'user id: {add_u}')

        db_user.update_user_username('baaa12sd1235467@added.ru', 'Super New')

        print(*db_auto.get_all_cars_in_db(), sep='\n')
        print(*db_user.get_all_users_in_db(), sep='\n')
        print(db_auto.get_car_by_car_id(11))
        print(db_user.get_user_by_user_id(13))
    except Exception as ex:
        print(ex)
    finally:
        db_auto.close()


def create_user():
    try:
        return User(input('Enter your name: '), input('Enter your email: '))
    except Exception as ex:
        print('User is not created!')
        raise ex


def create_car():
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


def remove_first_char_from_keys(dictionary):
    if not dictionary:
        raise TypeError('Empty field')
    return {(k[1:]): v for k, v in dictionary.items()}


if __name__ == '__main__':
    main()
