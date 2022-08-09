# Python code to read from MySQL Database

import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
from itertools import chain

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
    limit = 100
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
    return list_of_leaves


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


def retrieve_full_classification_of_item_ids(connection, list_of_item_ids):
    query = "SELECT ID, FullClassification FROM CustomsItem;"
    results, columns = read_query(connection, query)
    #list_of_ids = [str(x[0]) for x in results if str(x[0]) in list_of_item_ids]  # a generator that iterates over all tuples, from each tuple takes the first value
    #list_of_full_classifications = [str(x[1]) for x in results if str(x[0]) in list_of_item_ids]  # a generator that iterates over all tuples, from each tuple takes the second value
    list_of_tuples = [x for x in results if str(x[0]) in list_of_item_ids]
    #print(list_of_ids[0:10])
    #print(list_of_full_classifications[0:10])
    print(list_of_tuples[0:10])


def retrieve_parent(connection, customs_item_id):
    query = "SELECT ID, Parent_CustomsItemID FROM CustomsItem where CustomsBookTypeID = 1 and ID = '" + customs_item_id + "';"
    results, columns = read_query(connection, query)
    # assuming only 1 row in the result!
    parent_id = results[0][1]
    print("for item id", customs_item_id, "the parent is", parent_id)
    return parent_id


def retrieve_all_parents_of_item(connection, customs_item_id):
    idd = customs_item_id
    list_of_parents = list(customs_item_id)
    while True:
        parent_id = retrieve_parent(connection, idd)
        if parent_id == 0:
            break
        list_of_parents.append(str(parent_id))
        idd = str(parent_id)
    print("list of parents is", list_of_parents)
    return list_of_parents


def only_date(date1):
    date_time_str = str(date1)
    date_only = date_time_str.split(' ')[0]
    return date_only


def retrieve_regularity_inception(connection, req):
    query = "select * from RegularityInception where RegularityRequirementID='" + req['RegularityRequirementID'] + "';"
    results, columns = read_query(connection, query)
    print(columns)
    print(results)
    counter = 0
    inceptions = list()
    for row in results:
        incs = dict()
        incs['RegularityRequirementID'] = str(row[1])
        incs['RegularityInceptionID'] = str(row[0])
        incs['InterConditions']= str(row[2])
        if incs['InterConditions']=='1':
            incs['InterConditions']='1-All'
        elif incs['InterConditions']=='3':
            incs['InterConditions']='3-Alt'
        incs['personal'] = str(row[3])
        if incs['personal']=='1':
            incs['personal']='1-NO?'
        incs['description'] = row[4]
        inceptions.append(incs)
        counter = counter + 1
    print(inceptions)
    return inceptions


def retrieve_regularity_requirement(connection, item_id):
    """
    This method retrieves from SQL db the whole data that is displayed in the part of Regulatory Requirements.
    The logic here is based on our assumptions of how the web-site pages are created from the data.
    In some edge cases it is not yet complete.
    Known Issues:
    1. How exactly does the web-site decide which rows to include in the display?
       It is according to start-date and end-date, but in some cases it is not straight-forward
    """
    current_date = '2022-08-08'     # TODO not hard-coded
    # Note that the following query dictates the order of columns in the result, which is
    # relied on later when extracting data fom the result. So if you change the query,
    # you must change code below in this function.
    query = "select * from RegularityRequirement rr, RegularityInception ri, RegularityRequiredCertificate rrc " + \
            "where ri.RegularityRequirementID=rr.ID " + \
            "and rrc.RegularityInceptionID=ri.ID " + \
            "and rr.CustomsItemID='" + item_id + "';"
    results, columns = read_query(connection, query)
    print(columns)
    #('ID', 'TypeID', 'Title', 'State', 'CreateDate', 'CreateUserID', 'UpDatetimeDate', 'UpDatetimeUserID', 'OrganizationUnitID', 'CustomerID', 'CountryID', 'IsAllCountries', 'CustomsItemID', 'IsAllCustomsItems', 'IsLimitedCountryRegularityRequirement', 'StartDate', 'EndDate', 'MekachDate', 'InceptionCodeID', 'RegularityPublicationCodeID19', '20RegularitySourceCodeID', 'CustomsBookTypeID', 'MekachID', 'ID', 'RegularityRequirementID', 'InterConditionsRelationshipID', 'IsPersonalImportIncluded', 'RequirementGoodsDescription', 'RegularityRequirementWarningsID', 'IsCarnetIncluded', 'ID', 'RegularityInceptionID', 'ConfirmationTypeID', 'CNumber', 'TextualCondition', 'TrNumber', 'AuthorityID')
    #0: (3962, 0, 'TEMPORARILY_NULL', 0, datetime.datetime(2011, 6, 1, 0, 0), 0, datetime.datetime(1970, 1, 1, 2, 0), 0, 0, 0, 0, 1, 26074, 0, 0, datetime.datetime(2011, 6, 1, 0, 0), datetime.datetime(2069, 12, 31, 0, 0), datetime.datetime(1970, 1, 1, 2, 0), 1, 1, 2, 1, 0, 3499, 3962, 1, 1, ' ', 0, 0, 1818, 3499, 1, 0, '', 0, 1)
    #0: (5934, 0, 'TEMPORARILY_NULL', 0, datetime.datetime(2020, 3, 25, 0, 0), 0, datetime.datetime(1970, 1, 1, 2, 0), 0, 0, 0, 0, 1, 26074, 0, 0, datetime.datetime(2011, 6, 1, 0, 0), datetime.datetime(2069, 12, 31, 0, 0), datetime.datetime(1970, 1, 1, 2, 0), 1, 20, 2, 1, 0, 7108, 5934, 1, 1, ' ', 0, 0, 10310, 7108, 1, 0, '', 0, 1)

    counter = 0
    reqs = list()
    for row in results:
        # 'RegularityPublicationCodeID': '1' is Tosefet 2 LeZav Yevu Hofshi
        # 'RegularityPublicationCodeID': '20' is Tosefet 2 LeZav Yevu Ishi!!!
        print(str(counter), ":",row)
        d = dict()
        d['order'] = counter
        # column numbers below depend on the exact query hard-coded above!
        d['RegularityRequirementID'] = str(row[0])
        d['from_item'] = item_id    # TODO should be full classification of this id
        d['create_date'] = only_date(row[4])
        d['update_date'] = only_date(row[6])
        d['start_date'] = only_date(row[15])
        d['end_date'] = only_date(row[16])
        d['InceptionCodeID'] = str(row[18])
        d['RegularityPublicationCodeID'] = str(row[19])     # see comment above!!
        #'20RegularitySourceCodeID', 'CustomsBookTypeID', 'MekachID', 'ID', 'RegularityRequirementID', 'InterConditionsRelationshipID', 'IsPersonalImportIncluded', 'RequirementGoodsDescription', 'RegularityRequirementWarningsID', 'IsCarnetIncluded',
        # '30ID', 'RegularityInceptionID', 'ConfirmationTypeID', 'CNumber', 'TextualCondition', 'TrNumber', 'AuthorityID')
        d['RegularityInceptionID'] = str(row[23])
        d['InterConditions'] = str(row[25])
        if d['InterConditions']=='1':
            d['InterConditions']='1-All'
        elif d['InterConditions']=='3':
            d['InterConditions']='3-Alt'
        d['personal'] = str(row[26])    #1=Yes, 0=No
        if d['personal']=='1':
            d['personal']='1-Yes'
        elif d['personal']=='0':
            d['personal']='0-No'
        d['description'] = str(row[27])
        d['RegularityRequiredCertificateID'] = str(row[30])
        d['ConfirmationTypeID'] = str(row[32]) # (together with AuthorityID?) 1=0101(Vetrinary), 2=0102(HaganatHazomeach) 66=0701 67=0702 68=0703 70=0705 39=0305
        d['CNumber'] = str(row[33])
        d['TextualCondition'] = str(row[34])
        d['TrNumber'] = str(row[35])
        d['AuthorityID'] = str(row[36]) # 7=Misrad HaBriut, 1=Misrad HaChaklaut, 3=Misrad HaCalcala
        # append only lines in which current date is between d['start_date'] and d['end_date'] = only_date(row[16])
        reqs.append(d)
        # if current_date>d['start_date'] and current_date<d['end_date']:
        #     reqs.append(d)
        counter = counter + 1
    #print(reqs)
    return reqs

def retrieve_regularity_requirement1(connection, item_id):
    query = "select * from RegularityRequirement where CustomsItemID='" + item_id + "';"
    results, columns = read_query(connection, query)
    print(columns)
    counter = 0
    reqs = list()
    for row in results:
        print(str(counter), ":",row)
        d = dict()
        d['order'] = counter
        d['RegularityRequirementID'] = str(row[0])
        d['from_item'] = item_id    # TODO should be full classification of this id
        d['create_date'] = only_date(row[4])
        d['update_date'] = only_date(row[6])
        d['start_date'] = only_date(row[15])
        d['end_date'] = only_date(row[16])
        d['InceptionCodeID'] = str(row[18])
        d['RegularityPublicationCodeID'] = str(row[19])
        reqs.append(d)
        counter = counter + 1
    print(reqs)
    for req in reqs:
        retrieve_regularity_inception(connection, req)
    return reqs


def do_some_queries():
    connection = connect()
    if connection is None:
        exit(-1)
    #retrieve_customs_item_by_full_classification(connection, '4823691000')
    #retrieve_some_data_of_customs_item(connection, 'XV')
    #retrieve_parent_items_of_customs_item(connection, '4823691000')
    #retrieve_customs_item_by_full_classification(connection, 'XV')
    #retrieve_all_import_Full_Classifications_as_sorted_list(connection)
    list_of_ids = retrieve_only_leaves(connection)
    retrieve_full_classification_of_item_ids(connection, list_of_ids)
    list_of_parents = retrieve_all_parents_of_item(connection, list_of_ids[5])
    all_reqs = list()
    for item in list_of_parents:
        reqs = retrieve_regularity_requirement(connection, item)
        if len(reqs) == 0:
            continue
        all_reqs.append(reqs)
    #now flatten the list of lists
    flattened_list = list(chain.from_iterable(all_reqs))
    print(flattened_list)

def main():
    #do_simple_query()
    #do_dataframe_query()
    do_some_queries()





if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())



# for item_id=4 (full_classification=0407110000) I got:
# [
#     {'order': 0, 'RegularityRequirementID': '3962', 'from_item': '26074', 'create_date': '2011-06-01', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '1', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3499', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': ' ', 'RegularityRequiredCertificateID': '1818', 'ConfirmationTypeID': '1', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 1, 'RegularityRequirementID': '5934', 'from_item': '26074', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '1', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '7108', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': ' ', 'RegularityRequiredCertificateID': '10310', 'ConfirmationTypeID': '1', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 3, 'RegularityRequirementID': '4357', 'from_item': '20729', 'create_date': '2011-06-01', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1549', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'חלב ומוצרי חלב להזנת בעלי חיים', 'RegularityRequiredCertificateID': '1815', 'ConfirmationTypeID': '1', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 4, 'RegularityRequirementID': '4357', 'from_item': '20729', 'create_date': '2011-06-01', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1548', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים למעט 04.07 ו-04.08', 'RegularityRequiredCertificateID': '1816', 'ConfirmationTypeID': '66', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 5, 'RegularityRequirementID': '4357', 'from_item': '20729', 'create_date': '2011-06-01', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1548', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים למעט 04.07 ו-04.08', 'RegularityRequiredCertificateID': '1817', 'ConfirmationTypeID': '70', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 7, 'RegularityRequirementID': '6190', 'from_item': '20729', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2011-06-01', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '6072', 'InterConditions': '3-Alt', 'personal': '1-Yes', 'description': 'חלב ומוצרי חלב להזנת בעלי חיים', 'RegularityRequiredCertificateID': '10309', 'ConfirmationTypeID': '1', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'}
# ]

# for item_id=7 (full_classification=0701109100) I got:
# (7, '0701109100'), list of parents is ['7', '16156', '5642', '23464', '6118', '11984']
# [
#     {'order': 0, 'RegularityRequirementID': '3349', 'from_item': '23464', 'create_date': '2008-06-04', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1795', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '1840', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 1, 'RegularityRequirementID': '3349', 'from_item': '23464', 'create_date': '2008-06-04', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1794', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '1841', 'ConfirmationTypeID': '66', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 2, 'RegularityRequirementID': '3349', 'from_item': '23464', 'create_date': '2008-06-04', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1794', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '1842', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 3, 'RegularityRequirementID': '3349', 'from_item': '23464', 'create_date': '2008-06-04', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '1794', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '1843', 'ConfirmationTypeID': '70', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 4, 'RegularityRequirementID': '5646', 'from_item': '23464', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '6230', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '10326', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 5, 'RegularityRequirementID': '5646', 'from_item': '23464', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2008-06-04', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8278', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'אחרים', 'RegularityRequiredCertificateID': '10732', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1'}
# ]

# (9, '0712391000'), list of parents is ['9', '21870', '8925', '2069', '6118', '11984']
# [
#     {'order': 7, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3676', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '7113', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 8, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3677', 'InterConditions': '1-All', 'personal': '0', 'description': 'חתוכים, פרוסים, שבורים, בצרת אבקה', 'RegularityRequiredCertificateID': '7114', 'ConfirmationTypeID': '66', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 9, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3677', 'InterConditions': '1-All', 'personal': '0', 'description': 'חתוכים, פרוסים, שבורים, בצרת אבקה', 'RegularityRequiredCertificateID': '7115', 'ConfirmationTypeID': '70', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 10, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3675', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '7117', 'ConfirmationTypeID': '70', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 11, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3675', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '9990', 'ConfirmationTypeID': '66', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 16, 'RegularityRequirementID': '4670', 'from_item': '2069', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '7218', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '10631', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 17, 'RegularityRequirementID': '4670', 'from_item': '2069', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8288', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'אחרים', 'RegularityRequiredCertificateID': '10737', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1'},
#     {'order': 21, 'RegularityRequirementID': '1671', 'from_item': '2069', 'create_date': '2016-04-14', 'update_date': '1970-01-01', 'start_date': '2016-04-14', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3675', 'InterConditions': '1-All', 'personal': '0', 'description': 'אחרים', 'RegularityRequiredCertificateID': '13139', 'ConfirmationTypeID': '2', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1'}
# ]
#
# (12, '1701130000')
# list of parents is ['12', '2186', '14619', '11448', '16904']
#
# [
#     {'order': 2, 'RegularityRequirementID': '3546', 'from_item': '11448', 'create_date': '2009-05-10', 'update_date': '1970-01-01', 'start_date': '2009-05-10', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5023', 'InterConditions': '1-All', 'personal': '0', 'description': 'למאכל אדם', 'RegularityRequiredCertificateID': '2118', 'ConfirmationTypeID': '66', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 3, 'RegularityRequirementID': '3546', 'from_item': '11448', 'create_date': '2009-05-10', 'update_date': '1970-01-01', 'start_date': '2009-05-10', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5023', 'InterConditions': '1-All', 'personal': '0', 'description': 'למאכל אדם', 'RegularityRequiredCertificateID': '2119', 'ConfirmationTypeID': '70', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'},
#     {'order': 4, 'RegularityRequirementID': '3546', 'from_item': '11448', 'create_date': '2009-05-10', 'update_date': '1970-01-01', 'start_date': '2009-05-10', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5024', 'InterConditions': '1-All', 'personal': '0', 'description': 'המיועד לייצור תרופות', 'RegularityRequiredCertificateID': '2120', 'ConfirmationTypeID': '67', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '7'}
# ]
