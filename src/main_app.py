from datetime import datetime

import db_helper
from users import User
from cars import Car

now = datetime.now()


def main():
    car = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023')
    user = User('asdasd', 'asd123@added.ru')

    try:
        db = db_helper.AutoBotDB()
        add_u = db.add_user(*vars(user).values())
        # print(f'car id: {db.add_car(*vars(car).values())}')
        # print(f'user id: {add_u}')

        print(*db.get_all_cars_in_db(), sep='\n')
        print(*db.get_all_users_in_db(), sep='\n')
        print(db.get_car_by_car_id(11))
        print(db.get_user_by_user_id(13))
    except Exception as ex:
        print(ex)
    finally:
        db.close()

    # data_all = []
    #
    # try:
    #     add_user_to_db(create_user(), data_all)
    # except Exception as ex:
    #     print(ex)

    # try:
    #     add_car_to_user_in_db(find_user_with_email(data_all), Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023'))
    # except Exception as ex:
    #     print(ex)
    #
    # try:
    #     update_user_name_in_db(find_user_with_email(data_all))
    # except Exception as ex:
    #     print(ex)

    # print(data_all)


def create_user():
    try:
        return User(input('Enter your name: '), input('Enter your email: '))
    except Exception as ex:
        print('User is not created!')
        raise ex


def find_user_with_email(data_db):
    try:
        email_to_find = input('Enter user email to find: ')
        User.check_email(email_to_find)
        for user in data_db:
            if email_to_find == user['email']:
                return user
        raise TypeError('No user with this email')
    except Exception as ex:
        print('User not found')
        raise ex


def user_not_in_db(user_to_add, db):
    try:
        if db:
            u_emails = []
            for u in db:
                u_emails.append(u['email'])
            if user_to_add.email in u_emails:
                print(f'User with email: {user_to_add.email} already exist')
                return False
            else:
                print(f'User {user_to_add.email} is not in DB')
                return True
        else:
            print(f'User {user_to_add.email} is not in DB')
            return True
    except Exception as ex:
        print('User exist error')
        raise ex


def update_user_name_in_db(user):
    try:
        if user:
            print(f"Update user's name: {user['username']}")
            new_name = input('Enter new user name: ')
            User.not_empty_str(new_name)
            user['username'] = new_name.strip()
            print(f'User name updated to {user["username"]}')
        else:
            raise TypeError('No user selected')
    except Exception as ex:
        print('Error updating name!')
        raise ex


def add_user_to_db(user_to_add, db):
    try:
        if user_to_add:
            if user_not_in_db(user_to_add, db):
                db.append(remove_first_char_from_keys(vars(user_to_add)))
                print(f'User {user_to_add.username} added to DB')
        else:
            print('User is Empty, not added to DB')
            raise TypeError('User is Empty, not added to DB')
    except Exception as ex:
        print('User not added to DB')
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


def add_car_to_user_in_db(user, car_to_add):
    try:
        if user:
            if car_to_add:
                user.update(remove_first_char_from_keys(vars(car_to_add)))
                print((f'Car {car_to_add.model} {car_to_add.model_name} '
                       f'added to user {user["username"]} in DB'))
            else:
                print(f'Car is empty. Not added to user')
                raise TypeError('Car is empty. Not added to user')
        else:
            print(f'No such user to add a car')
            raise TypeError('No such user to add a car')
    except Exception as ex:
        print('Car not added to user in DB')
        raise ex


def remove_first_char_from_keys(dictionary):
    if not dictionary:
        raise TypeError('Empty field')
    return {(k[1:]): v for k, v in dictionary.items()}


if __name__ == '__main__':
    main()
