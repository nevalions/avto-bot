from psycopg2 import sql

import src.db.db_queries as queries
from src.db.db_main import AutoBotDB as Db


class AutoBotMainDB(Db):
    def add_car_to_user_in_db(self, user_id, car_id):
        try:
            query = queries.create_m2m_relation(user_id, car_id)
            self.query_execute(query)
            print(f'Car ID({car_id}) added to user ID({user_id})')
            # return user_id, car_id
        except Exception as ex:
            print(ex)
            print(f'Error adding car to user, user already have this car')

    def show_all_users_cars(self, _user_id):
        try:
            query = sql.SQL("SELECT car.id, car.model, car.model_name, car.mileage, "
                            "car.measures FROM user INNER JOIN user_car ON user_car.user_id=user.id INNER JOIN "
                            "cars ON user_car.car_id=car.id WHERE user.id={user_id};").format(
                user_id=sql.Literal(_user_id))

            result = self.select_query_dict(query)
            if result:
                return result
            else:
                raise TypeError('User dont have any car')
        except Exception as ex:
            print(ex)
