# Python code to read from MySQL Database

import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"MySQL Database connection successful (hostname='{host_name}', database name='{db_name}')")
    except Error as err:
        print(f"==> Error: '{err}'")
        print(f"==> maybe you need to start the database with: docker start mysql_server_custom_book")

    return connection


def connect():
    return create_db_connection("localhost", "evyatar_user", "123456", "my_db_1")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        column_names = cursor.column_names
        result = cursor.fetchall()
        return result, column_names
    except Error as err:
        print(f"Error: '{err}'")


def do_simple_query():
    # connection1 = create_server_connection("localhost", "evyatar_user", "123456")
    connection = create_db_connection("localhost", "evyatar_user", "123456", "my_db_1")

    if connection is None:
        exit(-1)

    q1 = """
        SELECT *
        FROM CustomsItem
        where FullClassification='8418200000';
        """

    results, columns = read_query(connection, q1)

    # results is a list of 3 items (3 rows in the result set)
    for result in results:
        # result is a tuple of 19 items (19 columns in the table 'CustomsItem')
        print(result)

    # you could convert each tuple to list with list()
    for result in results:
        row_as_list = list(result)
        print(row_as_list)

    # printing the headers (column names)
    print(columns)
    for result in results:
        print(result)


def do_query_to_dataframe(connection, query):
    results, columns = read_query(connection, query)

    # Returns a list of lists and then creates a pandas DataFrame
    from_db = []

    for result in results:
        result = list(result)
        from_db.append(result)

    df = pd.DataFrame(from_db, columns=columns)

    return df


def do_some_queries():
    connection = connect()
    if connection is None:
        exit(-1)
    retrieve_customs_item_by_full_classification(connection, '4823691000')
    retrieve_parent_items_of_customs_item(connection, '4823691000')


def do_dataframe_query():
    connection = create_db_connection("localhost", "evyatar_user", "123456", "my_db_1")

    if connection is None:
        exit(-1)

    q1 = """
            SELECT *
            FROM CustomsItem
            where FullClassification='8418200000';
            """
    df = do_query_to_dataframe(connection, q1)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df)
    print(df.to_string())   #to_string() prints the full dataFrame! good for small resultSets


def retrieve_customs_item_by_full_classification(connection, item_full_classification):
    query = "SELECT * FROM CustomsItem where FullClassification='" + item_full_classification + "';"
    df = do_query_to_dataframe(connection, query)
    print(query)
    print(df.to_string())
    return df

def retrieve_customs_item_by_item_id():
    pass


def retrieve_parent_items_of_customs_item(connection, item_full_classification):
    query = "SELECT * FROM CustomsItem where FullClassification='" + item_full_classification + "';"
    df = do_query_to_dataframe(connection, query)
    print(df["Parent_CustomsItemID"])
    print(df["CustomsItemHierarchicLocationID"])


def main():
    #do_simple_query()
    #do_dataframe_query()
    do_some_queries()





if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
