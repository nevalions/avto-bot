import psycopg2


def main():
    host = '127.0.0.1'
    user = 'avto'
    password = 'kicker'
    db_name = 'avtobot_db'
    port = '32777'
    query = 'SELECT * FROM test;'

    db_connect(host, user, password, db_name, port, query)


def db_connect(host, user, password, db_name, port, query):
    connect = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )
    cursor = connect.cursor()

    cursor.execute(query)

    connect.commit()


if __name__ == '__main__':
    main()