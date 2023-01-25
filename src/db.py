import psycopg2

from config import host, user, password, db_name


class AutoBotDB:
    """
    Main Postgres DB functions.
    """
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

    def select_list(self, query):
        pass

    def select_query_dict(self, query) -> dict:
        self.cursor.execute(query)
        columns = list(self.cursor.description)
        users_cars = self.cursor.fetchall()

        if users_cars:
            result = []
            for row in users_cars:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col.name] = row[i]
                result.append(row_dict)
            return result

    def close(self):
        self.cursor.close()
        self.connect.close()
