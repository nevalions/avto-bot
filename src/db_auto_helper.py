from db import AutoBotDB as Db
import db_main_queries as queries


class AutoBotAutoDB(Db):
    """
    Main Postgres DB functions for Car()
    """
    db_table_name = 'cars'

    def add_car(self, model: str, model_name: str, mileage: str, measures: str, date_added: str, description: str):
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
        self.cursor.execute(queries.get_all_rows_from_db(self.db_table_name))
        all_cars = self.cursor.fetchall()
        if all_cars:
            return all_cars
        else:
            print('No cars in DB')
            raise Exception

    def get_car_by_car_id(self, car_id):
        query = queries.get_db_item_by_id(self.db_table_name, car_id)
        self.cursor.execute(query)
        car = self.cursor.fetchall()
        if car:
            return car[0]
        else:
            print(f'No cars with ID {car_id}')
            raise Exception


def main():
    db = AutoBotAutoDB()
    try:
        print(db.get_all_cars_in_db())
    except Exception as ex:
        print(ex)
    finally:
        db.close()


if __name__ == '__main__':
    main()
