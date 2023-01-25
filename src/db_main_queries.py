from psycopg2 import sql


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


def get_all_rows_from_db(_table: str) -> sql:
    return sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(_table))
