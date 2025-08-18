import sqlite3
import constants

DB_NAME = ':memory:' if constants.IN_MEMORY_DB else 'scouting_app.db'

def get_connection():
    conn=sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def insert_data(table, args, data):
    conn = get_connection()
    cursor = conn.cursor()

    if (len(data) != len(args)):
        raise ValueError("Data length does not match arguments length")

    if isinstance(args, list):
        placeholders = ', '.join(['?'] * len(args))
        query = f'INSERT INTO {table} ({", ".join(args)}) VALUES ({placeholders})'
        cursor.execute(query, data)
        print(f'Inserted data into {table}: {data}')

    conn.commit()
    conn.close()

def get_recent_data(table, table_id, columns, limit=10):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = ''
    if isinstance(columns, list):
        query = 'SELECT {} FROM {}'.format(', '.join(columns), table)
    elif isinstance(columns, str):
        query = 'SELECT {} FROM {}'.format(columns, table)
    else:
        query = 'SELECT * FROM {}'.format(table)

    cursor.execute("PRAGMA foreign_key_list({})".format(table))
    foreign_key_list = cursor.fetchall()

    for fk in foreign_key_list:
        ref_table = fk[2]
        from_col = fk[3]
        to_col = fk[4]
        query += f' JOIN {ref_table} ON {table}.{from_col} = {ref_table}.{to_col}'

    query += f' ORDER BY {table}.{table_id} DESC'
    
    print(query)
    cursor.execute(query)
    rows = cursor.fetchmany(limit)
    conn.close()
    return rows

def search_data(base_table, search_type, search_query, operator = "=", cols = [], limit = 10):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(cols)

    query = 'SELECT {} FROM {}'.format(', '.join(cols), base_table)

    foreign_key_list = cursor.execute("PRAGMA foreign_key_list({})".format(base_table)).fetchall()
    for fk in foreign_key_list:
        ref_table = fk[2]
        from_col = fk[3]
        to_col = fk[4]
        query += f' JOIN {ref_table} ON {base_table}.{from_col} = {ref_table}.{to_col}'

    query += f" WHERE {search_type} {operator} ?"

    print(query, (search_query,))
    cursor.execute(query, (search_query,))
    rows = cursor.fetchmany(limit)
    conn.close()
    return rows

def create_table(table_name, columns, special_args=None):
    conn = get_connection()
    cursor = conn.cursor()

    column_defs = [f"{name} {dtype}" for name, dtype in columns.items()]
    if special_args:
        column_defs.extend(special_args)

    query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_defs)});'

    cursor.execute(query)
    print(f'Creating table {table_name} with query: {query}')
    conn.commit()
    conn.close()

def get_column_descriptions(table):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    conn.close()
    return columns

def get_id_by_arg(id_type, table, param, arg):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT {} FROM {} WHERE \"{}\" = ?".format(id_type, table, param), (arg,))
    row = cursor.fetchone()

    if row:
        id = row[0]
    else:
        cursor.execute("INSERT INTO {} ({}) VALUES (?)".format(table, param), (arg,))
        id = cursor.lastrowid

    conn.commit()
    conn.close()
    return id

def get_arg_by_id(id_type, table, param, arg):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT {} FROM {} WHERE {} = ?".format(param, table, id_type), (arg,))
    row = cursor.fetchone()

    if row:
        _arg = row[0]
    else:
        cursor.execute("INSERT INTO {} ({}) VALUES (?)".format(table, param), (arg,))
        _arg = arg

    conn.commit()
    conn.close()
    return _arg