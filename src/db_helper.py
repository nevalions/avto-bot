import psycopg2
from psycopg2 import sql

from config import host, user, password, db_name
import db_main_queries as queries


class AutoBotDB:
    users_db_table_name = 'users'
    cars_db_table_name = 'cars'

    def __init__(self, host_db=host, user_db=user, pass_db=password, db=db_name):
        self.host_db = host_db
        self.user_db = user_db
        self.pass_db = pass_db
        self.db = db

        self.connect = psycopg2.connect(
            host=host_db,
            user=user_db,
            password=pass_db,
            database=db
        )
        self.cursor = self.connect.cursor()

    def query_execute(self, query):
        self.cursor.execute(query)
        self.connect.commit()

    def add_user(self, _username, _email):
        try:
            query = sql.SQL("INSERT INTO users(username, email) SELECT {username}, {email} WHERE NOT EXISTS (SELECT "
                            "id FROM users WHERE email = {email})").format(username=sql.Literal(_username),
                                                                           email=sql.Literal(_email))

            self.cursor.execute(query)
            self.connect.commit()
            print(f'{_username} with ID: user_id added to DB')
        except Exception as ex:
            print(ex)
            print(f'Error adding user to DB')

    def get_all_users_in_db(self):
        self.cursor.execute(queries.get_all_rows_from_db(self.users_db_table_name))
        all_users = self.cursor.fetchall()
        if all_users:
            return all_users
        else:
            print('No users in DB')
            raise Exception

    def get_user_by_user_id(self, user_id):
        query = queries.get_db_item_by_id(self.users_db_table_name, user_id)
        self.cursor.execute(query)
        car = self.cursor.fetchall()
        if car:
            return car[0]
        else:
            print(f'No users with ID {user_id}')
            raise Exception

    def add_car(self, model, model_name, mileage, measures, date_added, description):
        try:
            query = "INSERT INTO cars(model, model_name, mileage, measures, date_added, description) " \
                    "VALUES(%s,%s,%s,%s,%s,%s) RETURNING id;"
            self.cursor.execute(query, (model, model_name, int(mileage), measures, date_added, description))
            self.connect.commit()
            car_id = self.cursor.fetchone()[0]
            print(f'{model} {model_name} added to DB')
            return car_id
        except Exception as ex:
            print(ex)
            print(f'Error adding car to DB')

    def get_all_cars_in_db(self):
        self.cursor.execute(queries.get_all_rows_from_db(self.cars_db_table_name))
        all_cars = self.cursor.fetchall()
        if all_cars:
            return all_cars
        else:
            print('No cars in DB')
            raise Exception

    def get_car_by_car_id(self, car_id):
        query = queries.get_db_item_by_id(self.cars_db_table_name, car_id)
        self.cursor.execute(query)
        car = self.cursor.fetchall()
        if car:
            return car[0]
        else:
            print(f'No cars with ID {car_id}')
            raise Exception

    def close(self):
        self.cursor.close()
        self.connect.close()


def main():
    try:
        db = AutoBotDB()
        # print(db.get_car_by_car_id(11))
        print(db.get_all_cars_in_db())
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
