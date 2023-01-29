from psycopg2 import sql


def create_m2m_relation(_id_one, _id_two):
    return sql.SQL("INSERT INTO users_cars VALUES ({id_one},{id_two}) RETURNING {id_one}, {id_two};").format(
        id_one=sql.Literal(_id_one),
        id_two=sql.Literal(_id_two)
    )


def update_str_value_in_db_by_key(_table: str, _key_name: str, _key: str, _value_name: str, _new_value: str) -> sql:
    """
    Update value in table DB, select by key: key_name, select value by value in item.
    Enter a new value
    :param _table:
    :param _key_name:
    :param _key:
    :param _value_name:
    :param _new_value:
    :return sql:
    """
    return sql.SQL("UPDATE {table} SET {value_name}={new_value} WHERE {key_name}={key} RETURNING id;").format(
        table=sql.Identifier(_table),
        key_name=sql.Identifier(_key_name),
        key=sql.Literal(_key),
        value_name=sql.Identifier(_value_name),
        new_value=sql.Literal(_new_value)
    )


def get_db_item_by_id(_table: str, _id: int) -> sql:
    return sql.SQL("SELECT * FROM {table} WHERE {table}.id={item_id}").format(
        table=sql.Identifier(_table),
        item_id=sql.Literal(_id)
    )


def get_db_item_by_name(_table: str, _item_name: str, _item: int) -> sql:
    return sql.SQL("SELECT * FROM {table} WHERE {table}.{item_name}={item}").format(
        table=sql.Identifier(_table),
        item_name=sql.Identifier(_item_name),
        item=sql.Literal(_item)
    )


def get_all_rows_from_db(_table: str) -> sql:
    return sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(_table))
