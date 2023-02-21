import mock
import builtins
import os
import sys
import pytest
# sys.path.append(os.path.join(os.getcwd(), '../..'))

from src.classes import app_no_sql as main_app
from src.classes.cars import Car
from src.classes.users import User


def main():
    test_find_user_with_email()
    test_user_not_in_db()
    test_update_user_name_in_db()
    test_add_user_to_db()
    test_add_car_to_user_in_db()
    test_remove_first_char_from_keys()

    test_find_user_with_email_ex()
    test_user_not_in_db_ex()
    test_update_user_name_in_db_ex()
    test_add_user_to_db_ex()
    test_add_car_to_user_in_db_ex()
    test_remove_first_char_from_keys_ex()


def test_find_user_with_email():
    test_users = [
        {'username': 'Test', 'email': 'asd@asd.ru'},
        {'username': 'Jhon', 'email': 'user@add.ru'}]

    with mock.patch.object(builtins, 'input', lambda _: 'asd@asd.ru'):
        assert main_app.find_user_with_email(test_users) == {
            'username': 'Test', 'email': 'asd@asd.ru'}
    with mock.patch.object(builtins, 'input', lambda _: 'user@add.ru'):
        assert main_app.find_user_with_email(test_users) == {
            'username': 'Jhon', 'email': 'user@add.ru'}


def test_user_not_in_db():
    db = [{'username': 'Test', 'email': 'asd@asd.ru'}]
    user_new = User('Jhon', 'user@add.ru')
    user_double = User('Test', 'asd@asd.ru')

    assert main_app.user_not_in_db(user_new, db) == True
    assert main_app.user_not_in_db(user_double, db) == False


def test_update_user_name_in_db():
    user = {'username': 'Jhon', 'email': 'user@add.ru'}
    user2 = {'username': 'Test', 'email': 'asd@asd.ru'}
    with mock.patch.object(builtins, 'input', lambda _: 'AAA'):
        main_app.update_user_name_in_db(user)
        assert user == {'username': 'AAA', 'email': 'user@add.ru'}
    with mock.patch.object(builtins, 'input', lambda _: 'BBB'):
        main_app.update_user_name_in_db(user2)
        assert user2 == {'username': 'BBB', 'email': 'asd@asd.ru'}


def test_add_user_to_db():
    db = []
    test_user1 = User('Test', 'asd@asd.ru')
    test_user2 = User('Jhon', 'user@add.ru')

    main_app.add_user_to_db(test_user1, db)
    assert db == [{'username': 'Test', 'email': 'asd@asd.ru'}]
    main_app.add_user_to_db(test_user2, db)
    assert db == [{'username': 'Test', 'email': 'asd@asd.ru'},
                  {'username': 'Jhon', 'email': 'user@add.ru'}]


def test_add_car_to_user_in_db():
    user1 = {'username': 'Test', 'email': 'asd@asd.ru'}
    car1 = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BlaBlaBla', '300000')
    main_app.add_car_to_user_in_db(user1, car1)
    assert user1 == {'username': 'Test',
                     'email': 'asd@asd.ru',
                     'model': 'Gmc',
                     'model_name': 'Savana',
                     'mileage': '300000',
                     'measures': 'miles',
                     'date_added': '22.01.2023',
                     'current_mileage': '300000',
                     'description': 'BlaBlaBla',
                     }


def test_remove_first_char_from_keys():
    test_dict = {'_asd': '_asd', '_12ASD': '12ASDASD'}
    assert main_app.remove_first_char_from_keys(test_dict) == {
        'asd': '_asd', '12ASD': '12ASDASD'}


"""test Exception raise"""


def test_find_user_with_email_ex():
    test_users = [
        {'username': 'Test', 'email': 'asd@asd.ru'},
        {'username': 'Jhon', 'email': 'user@add.ru'}]
    with pytest.raises(Exception):
        with mock.patch.object(builtins, 'input', lambda _: 'a@asd.ru'):
            assert main_app.find_user_with_email(test_users)


def test_user_not_in_db_ex():
    db = 'Not DB'
    with pytest.raises(Exception):
        user_new = User('Jhon', 'user@add.ru')
        main_app.user_not_in_db(user_new, db)


def test_update_user_name_in_db_ex():
    user = {'username': 'Jhon', 'email': 'user@add.ru'}
    with pytest.raises(Exception):
        with mock.patch.object(builtins, 'input', lambda _: 'A'):
            main_app.update_user_name_in_db(user)
    with pytest.raises(Exception):
        with mock.patch.object(builtins, 'input', lambda _: '           '):
            main_app.update_user_name_in_db(user)


def test_add_user_to_db_ex():
    db = [{'username': 'Test', 'email': 'asd@asd.ru'}]
    user_double = {'username': 'Test', 'email': 'asd@asd.ru'}
    try:
        test_user1 = User('Test2', '')
    except:
        pass

    with pytest.raises(Exception):
        main_app.add_user_to_db(test_user1, db)
    with pytest.raises(Exception):
        main_app.add_user_to_db(user_double, db)


def test_add_car_to_user_in_db_ex():
    try:
        not_user = User('', '')
        not_car = Car('', 'Savana', 300000, 'miles', '22.01.2023', 'BlaBlaBla', '300000')
    except:
        pass
    user1 = {'username': 'Test', 'email': 'asd@asd.ru'}
    car1 = Car('Gmc', 'Savana', '300000', 'miles', '22.01.2023', 'BlaBlaBla', '300000')

    with pytest.raises(Exception):
        main_app.add_car_to_user_in_db(not_user, car1)
    with pytest.raises(Exception):
        main_app.add_car_to_user_in_db(user1, not_car)
    with pytest.raises(Exception):
        main_app.add_car_to_user_in_db(not_user, not_car)


def test_remove_first_char_from_keys_ex():
    test_dict = {}
    with pytest.raises(Exception):
        main_app.remove_first_char_from_keys(test_dict)


if __name__ == '__main__':
    main()
