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


def retrieve_sons(connection, itemId):
    query = "SELECT ID FROM CustomsItem where CustomsBookTypeID = 1 and Parent_CustomsItemID=" + itemId + ";"
    results, columns = read_query(connection, query)
    return results


def retrieve_only_leaves(connection):
    limit = 1000
    count = 0
    query = "SELECT ID FROM CustomsItem where CustomsBookTypeID = 1 and FullClassification not like '-%';"
    results, columns = read_query(connection, query)
    print("there are", len(results), "items with CustomsBookTypeID=import")
    # a generator that iterates over all tuples, from each tuple takes the first value
    list_of_ids = [str(x[0]) for x in results]
    print("there are", len(list_of_ids), "items with CustomsBookTypeID=import")
    print("searching leaves in first", limit, "items...")
    list_of_leaves = []
    for itemId in list_of_ids:
        count = count + 1
        if count >= limit:
            break
        sons = retrieve_sons(connection, itemId)
        if len(sons) == 0:
            list_of_leaves.append(itemId)
            #print("item", itemId, "has no sons")
    howManyLeaves = len(list_of_leaves)
    print("found", howManyLeaves, "leaves in", limit, "items")
    print(list_of_leaves[0:10])


def retrieve_all_import_Full_Classifications_as_sorted_list(connection):
    # query only those at the leaves (there is no other item that has them as parents)
    query = "SELECT FullClassification, ID as itemId FROM CustomsItem a where CustomsBookTypeID = 1 and FullClassification not like '-%' ;"
    results, columns = read_query(connection, query)
    print("there are", len(results), "items with CustomsBookTypeID=import")
    # a generator that iterates over all tuples, from each tuple takes the first value
    list_of_full_classifications = [str(x[0]) for x in results]
    list_of_full_classifications.sort()
    print('-> returning', list_of_full_classifications[0:10])
    return list_of_full_classifications


def retrieve_all_import_Full_Classifications_as_sorted_list1(connection):
    query = "SELECT FullClassification FROM CustomsItem where CustomsBookTypeID = 1 and FullClassification not like '-%';"
    results, columns = read_query(connection, query)
    print("there are", len(results), "items with CustomsBookTypeID=import")
    # a generator that iterates over all tuples, from each tuple takes the first value
    list_of_full_classifications = [str(x[0]) for x in results]
    list_of_full_classifications.sort()
    print('-> returning', list_of_full_classifications[0:10])
    return list_of_full_classifications


def retrieve_parent_items_of_customs_item(connection, item_full_classification):
    query = "SELECT FullClassification FROM CustomsItem;"
    results, columns = read_query(connection, query)
    print("there are", len(results), "custom items")
#    query = "SELECT FullClassification FROM CustomsItem where CustomsBookTypeID = 1;"
    # there are items with fullClassifications starting with - such as '-0010000000', '-0030000000'
    query = "SELECT FullClassification FROM CustomsItem where CustomsBookTypeID = 1 and FullClassification not like '-%';"
    results, columns = read_query(connection, query)
    print("there are", len(results), "items with CustomsBookTypeID=import")
    list_of_full_classifications = [str(x[0]) for x in results]  # a generator that iterates over all tuples, from each tuple takes the first value
    list_of_full_classifications.sort()
    print(list_of_full_classifications[0:10])

def retrieve_items_of_customs_item(connection, item_full_classification):
    query = "SELECT FullClassification FROM CustomsItem;"
    query2 = "SELECT FullClassification, ID FROM CustomsItem;"      # this would work with same results - because all tuples will have 2 members, but we take the first
    query3 = "SELECT ID, FullClassification FROM CustomsItem;"      # this would work with similar results - give list of all IDs instead of all full-classifications
    results, columns = read_query(connection, query)
    numberOfItems = len(results)
    tuple_of_first_row = results[0]     # ('5205230000',)
    value_of_first_field_of_first_row = results[0][0]     # '5205230000'

    list_of_full_classifications = [str(x[0]) for x in results]  # a generator that iterates over all tuples, from each tuple takes the first value
    print(list_of_full_classifications[0:10])
    # sorts the list in-place!!
    list_of_full_classifications.sort(reverse=False)
    print(list_of_full_classifications[0:100])   # result is ['-0010000000', '-0030000000', '-0031000000', '-0031100000', '-0031900000', '-0039000000', '-0040000000', '-0041000000', '-0041100000', '-0041900000']
    list_of_full_classifications.sort(reverse=True)
    print(list_of_full_classifications[0:40])   # result is ['XXII', 'XXII', 'XXI', 'XXI', 'XX', 'XX', 'XX', 'XVIII', 'XVIII', 'XVIII']


    # results is a list of 3 items (3 rows in the result set)
    #for result in results:
    #    print(result)


def retrieve_some_data_of_customs_item(connection, item_full_classification):
    # CustomsBookTypeID could be 1 or 2 or 3
    # selecting a customItem based on its FullClassification is not enough (not unique)
    # you must add AND CustomsBookTypeID=1 (1 = import)
    query = "SELECT * FROM CustomsItem where FullClassification='" + item_full_classification + "';"
    df = do_query_to_dataframe(connection, query)
    print("result has", df.shape[0], "rows and", df.shape[1], "columns")

    query = "SELECT * FROM CustomsItem where FullClassification='" + item_full_classification + "' and CustomsBookTypeID = 1;"
    df = do_query_to_dataframe(connection, query)
    print("result has", df.shape[0], "rows and", df.shape[1], "columns")

    # assuming result has 1 row:
    print('ID:', df.loc[0, 'ID'])
    print('FullClassification:', df.loc[0, 'FullClassification'])
    print('Parent_CustomsItemID:', df.loc[0, 'Parent_CustomsItemID'])
    print('CustomsItemHierarchicLocationID:', df.loc[0, 'CustomsItemHierarchicLocationID'])
    print('CustomsBookTypeID:', df.loc[0, 'CustomsBookTypeID'])
    #print(df["Parent_CustomsItemID"])
    #print(df["CustomsItemHierarchicLocationID"])


def do_some_queries():
    connection = connect()
    if connection is None:
        exit(-1)
    #retrieve_customs_item_by_full_classification(connection, '4823691000')
    #retrieve_some_data_of_customs_item(connection, 'XV')
    #retrieve_parent_items_of_customs_item(connection, '4823691000')
    #retrieve_customs_item_by_full_classification(connection, 'XV')
    #retrieve_all_import_Full_Classifications_as_sorted_list(connection)
    retrieve_only_leaves(connection)


def main():
    #do_simple_query()
    #do_dataframe_query()
    do_some_queries()





if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
