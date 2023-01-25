from psycopg2 import sql

import db_queries as queries
from db import AutoBotDB as Db


class AutoBotMainDB(Db):
    def add_car_to_user_in_db(self, user_id, car_id):
        try:
            query = queries.create_m2m_relation(user_id, car_id)
            self.query_execute(query)
            print(f'Car ID({car_id}) added to user ID({user_id})')
            return user_id, car_id
        except Exception as ex:
            print(ex)
            print(f'Error adding car to user, user already have this car')

    def show_all_users_cars(self, _user_id):
        try:
            query = sql.SQL("SELECT cars.id, cars.model, cars.model_name, cars.mileage, "
                            "cars.measures FROM users INNER JOIN users_cars ON users_cars.user_id=users.id INNER JOIN "
                            "cars ON users_cars.car_id=cars.id WHERE users.id={user_id};").format(
                user_id=sql.Literal(_user_id))

            result = self.select_query_dict(query)
            if result:
                return result
            else:
                raise TypeError('User dont have any car')
        except Exception as ex:
            print(ex)

