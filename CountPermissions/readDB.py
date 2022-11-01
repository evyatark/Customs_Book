# Python code to read from MySQL Database

import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
from itertools import chain


full_classification_of_item_ids_cache = dict()
item_id_of_full_classification_cache = dict()
parents_of_items_cache = dict()

known_confirmation_id=(        # ConfirmationTypeID (together with AuthorityID?):
        1, 2, 3, 4, 5, 7, 9, 10, 16, 18,
    19, 22, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36, 37, 39, 40, 41, 42, 43, 44, 47,
    53, 54, 58, 60, 61, 62, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 78, 80, 82,
    87, 89, 91, 96, 98, 101, 103, 106, 109, 113, 118, 123, 515, 516, 517, 519, 520, 522, 524, 526, 527, 532
        )
all_conf_ids = [1, 2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40, 41, 42, 43, 44, 47, 49, 50, 51, 52, 53, 54, 58, 60, 61, 62, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 82, 84, 86, 87, 89, 91, 96, 98, 99, 101, 103, 105, 106, 108, 109, 113, 116, 118, 120, 121, 123, 505, 515, 516, 517, 518, 519, 520, 521, 522, 524, 526, 527, 528, 532]


# 1=0101(Vetrinary), 2=0102(HaganatHazomeach), 3=0103(Ishur Tiv Mispo), 4=0104(Ishur Mikun VeTechnologia)
# 7=0107 (Ishur Mancal Chaklaut)
# 5=0105 6= 9=0109 10=0110 13= 14= 15=
# 16= aaa אישור יצוא שירותים להגנת הצומח (without code!!) (Misrad HaChaklaut)
# 18=0201, 19=0204 (Maabada Musmechet LeRechev)
# 20= 21=
# 22=0207 (Ishur Mankal Tachbura)
# 24=0209 (Vaada Bein Misradit LeHetkenei Tnuah VeBetichut)
# 25=0210 26=0212 27=0213 28=0214
# 29=0215 (Rishayon Otonomia)  30=, 31=0217, 32=0218,
# 33= aaa רשיון יצוא אגף הרכב ושירותי תחזוקה - צמ"ה (without code!!)
# 34=0202 (Rishayon Agaf Rechev... Gaf Zamah)
# 36=0302 (Ishur Midot VeMishkalot) 37=0303
# 39=0305, 40=0307, 41=0308, 42=0309. 43=0310, 44=0311
# 47=0315 49= 50= 51= 52=
# 53=0402 (Machon HaTkanim Ishur LeShichrur)
# 54=Ishur Mafmac "" "אישור מפמכ"  (without code!!!)
# 58=0501 aaa "רשות המיסים אישור מנהל"
# 60=0602
# 61=0603 (Ishur Memune Al HaKrina)
# 62=0604 64= 65=
# 66=0701 67=0702 68=0703 69=0704 70=0705 71=0706 72=0708 73=0709 (Ishur Mancal Briut) 74=0710
# 75= aaa רשיון יבוא מלשכת הבריאות בנפת רמלה (without code!!)
# 76 77
# 78=0802 (Misrad HaBitachon)
# 80= aaa אישור הועדה לאנרגיה אטומית (without code!!)
# 82=1001 aaa אישור אגף ניהול משאבי תשתיות במשרד האנרגיה
# 84 86
# 87=1101 (Teudat Hechsher)
# 89=1201 aaa אישור בטחון פנים
# 91=1301 (IshurTikshoretSpectrum)
# 96= (Misrad HaTarbut VeHaSport?) אישור מנכל המדע התרבות והספורט (without code!!)
# 98= (Misrad HaChinuch?) אישור מנכל חינוך (without code!!)
# 99
# 101 aaa אישור מנכל בינוי ושיכון (without code!!) (Misrad HaShikun)
# 103= aaa רשיון יבוא (without code!!) AuthorityID=19
# 105
# 106=2101 aaa אישור רשות העתיקות
# 108
# 109=0325 (Ishur Sichrur)
# 113=1203(Rishayon Agaf Pikuach VeRishuy Klei Yeriyah)
# 116
# 118=0713
# 120 121
# 123=2301 (HaMinhal HaEzrachi Ishur Kamat Tikshoret)
# 505 515=0804(Rishayon LeYevu Amlach)
# 516=0219 (Ishur Agaf Harechev ... Gaf Zamah)
# 517=0203
# 518
# 519=0221, 520=0222 (Rishayon Rashut HaSapanut VeHanmalim)
# 521
# 522=2402 (IshurSichrurMutne Maabadot)
# 524=0715 aaa רשיון לתכשיר לפי צו תכשירים להדברת מזיקים לאדם
# 526=2303 (Ishur Kamat Haganat HaSviva)
# 527=0319 (Ishur Hatarat Ziud Du Shimushi LeTchumei HaRashap)
# 528,
# 532=1204 aaa אישור מפקח על הכבאות
ConfirmationTypeID_table = dict()
ConfirmationTypeID_table['1'] = "0101"
ConfirmationTypeID_table['2'] = "0102"
ConfirmationTypeID_table['3'] = "0103"
ConfirmationTypeID_table['4'] = "0104"
ConfirmationTypeID_table['5'] = "0105"
ConfirmationTypeID_table['7'] = "0107"
ConfirmationTypeID_table['9'] = "0109"
ConfirmationTypeID_table['10'] = "0110"
ConfirmationTypeID_table['16'] = "אישור יצוא שירותים להגנת הצומח"
ConfirmationTypeID_table['18'] = "0201"
ConfirmationTypeID_table['19'] = "0204"
ConfirmationTypeID_table['22'] = "0207"
ConfirmationTypeID_table['24'] = "0209"
ConfirmationTypeID_table['25'] = "0210"
ConfirmationTypeID_table['26'] = "0212"
ConfirmationTypeID_table['27'] = "0213"
ConfirmationTypeID_table['28'] = "0214"
ConfirmationTypeID_table['29'] = "0215"
ConfirmationTypeID_table['31'] = "0217"
ConfirmationTypeID_table['32'] = "0218"
ConfirmationTypeID_table['33'] = 'רשיון יצוא אגף הרכב ושירותי תחזוקה - צמ"ה'
ConfirmationTypeID_table['34'] = "0202"
ConfirmationTypeID_table['36'] = "0302"
ConfirmationTypeID_table['37'] = "0303"
ConfirmationTypeID_table['39'] = "0305"
ConfirmationTypeID_table['40'] = "0307"
ConfirmationTypeID_table['41'] = "0308"
ConfirmationTypeID_table['42'] = "0309"
ConfirmationTypeID_table['43'] = "0310"
ConfirmationTypeID_table['44'] = "0311"
ConfirmationTypeID_table['47'] = "0315"
ConfirmationTypeID_table['53'] = "0402"
ConfirmationTypeID_table['54'] = "אישור מפמכ"
ConfirmationTypeID_table['58'] = "0501"
ConfirmationTypeID_table['60'] = "0602"
ConfirmationTypeID_table['61'] = "0603"
ConfirmationTypeID_table['62'] = "0604"
ConfirmationTypeID_table['66'] = "0701"
ConfirmationTypeID_table['67'] = "0702"
ConfirmationTypeID_table['68'] = "0703"
ConfirmationTypeID_table['69'] = "0704"
ConfirmationTypeID_table['70'] = "0705"
ConfirmationTypeID_table['71'] = "0706"
ConfirmationTypeID_table['72'] = "0708"
ConfirmationTypeID_table['73'] = "0709"
ConfirmationTypeID_table['74'] = "0710"
ConfirmationTypeID_table['75'] = "רשיון יבוא מלשכת הבריאות בנפת רמלה"
ConfirmationTypeID_table['78'] = "0802"
ConfirmationTypeID_table['80'] = "אישור אגף ניהול משאבי תשתיות"     # במשרד האנרגיה
ConfirmationTypeID_table['82'] = "1001"
ConfirmationTypeID_table['87'] = "1101"
ConfirmationTypeID_table['89'] = "1201"
ConfirmationTypeID_table['91'] = "1301"
ConfirmationTypeID_table['96'] = "אישור מנכל המדע התרבות והספורט"
ConfirmationTypeID_table['98'] = "אישור מנכל חינוך"
ConfirmationTypeID_table['101'] = "אישור מנכל בינוי ושיכון"
ConfirmationTypeID_table['103'] = "רשיון יבוא"
ConfirmationTypeID_table['106'] = "2101"
ConfirmationTypeID_table['109'] = "0325"
ConfirmationTypeID_table['113'] = "1203"
ConfirmationTypeID_table['118'] = "0713"
ConfirmationTypeID_table['123'] = "2301"
ConfirmationTypeID_table['515'] = "0804"
ConfirmationTypeID_table['516'] = "0219"
ConfirmationTypeID_table['517'] = "0203"
ConfirmationTypeID_table['519'] = "0221"
ConfirmationTypeID_table['520'] = "0222"
ConfirmationTypeID_table['522'] = "2402"
ConfirmationTypeID_table['524'] = "0715"
ConfirmationTypeID_table['526'] = "2303"
ConfirmationTypeID_table['527'] = "0319"
ConfirmationTypeID_table['532'] = "1204"
#ConfirmationTypeID_table[''] = ""


# RegularityPublicationCodeID column
# המקור החוקי לדרישה
# 'RegularityPublicationCodeID': '1'  is Tosefet 2 LeZav Yevu Hofshi תוספת 2 לצו יבוא חופשי
# 3  "Hakika Acheret LeZav Matan Rishyonot Yevu" חקיקה אחרת לצו מתן רשיונות יבוא
# 'RegularityPublicationCodeID': '7' is "Ishur Mancal LeTaarif Meches" אישור מנכל לתעריף מכס
# RegularityPublicationCodeID    '16' is "Hakika Acheret LeZav Aluf"     חקיקה אחרת לצו אלוף
# 'RegularityPublicationCodeID': '20' is Tosefet 2 LeZav Yevu Ishi!!!   תוספת 2 לצו יבוא אישי
RegularityPublicationCode_table = dict()
RegularityPublicationCode_table['1'] = "תוספת 2 לצו יבוא חופשי"
RegularityPublicationCode_table['3'] = "חקיקה אחרת לצו מתן רשיונות יבוא"
RegularityPublicationCode_table['7'] = "אישור מנכל לתעריף מכס"
RegularityPublicationCode_table['16'] = "חקיקה אחרת לצו אלוף"
RegularityPublicationCode_table['20'] = "תוספת 2 לצו יבוא אישי"

# AuthorityID
# 1=Misrad HaChaklaut, 2=Misrad HaTachbura 3=Misrad HaCalcala 4=MachonHaTkanim 5=Rashut Hamisim 6=HaMisrad LeHaganat HaSviva
# 7=Misrad HaBriut, 8=Misrad HaBitachon 9=Misrad Roham 10=Misrad HaEnergia 11=Rabanut Roshit 12=Misrad Bitachon Pnim
# 13=Misrad HaTikshoret 15=Misrad HaTarbut VeHaSport(?) 16=Misrad HaChinuch(?) 18=Misrad HaShikun
# 19=aaa נציגות קונסולרית ישראלית בחוץ לארץ
# 21=Rashut HaAtikot 23=Haminhal HaEzrachi 24=MaabedetBdika
AuthorityID_table = dict()
AuthorityID_table['1'] = "משרד החקלאות"
AuthorityID_table['2'] = "משרד התחבורה"
AuthorityID_table['3'] = "משרד הכלכלה"
AuthorityID_table['4'] = "מכון התקנים"
AuthorityID_table['5'] = "רשות המיסים"
AuthorityID_table['6'] = "המשרד להגנת הסביבה"
AuthorityID_table['7'] = "משרד הבריאות"
AuthorityID_table['8'] = "משרד הבטחון"
AuthorityID_table['9'] = "משרד ראש הממשלה"
AuthorityID_table['10'] = "משרד האנרגיה"
AuthorityID_table['11'] = "הרבנות הראשית"
AuthorityID_table['12'] = "המשרד לבטחון פנים"
AuthorityID_table['13'] = "משרד התקשורת"
AuthorityID_table['15'] = "משרד התרבות והספורט"
AuthorityID_table['16'] = "משרד החינוך"
AuthorityID_table['18'] = "משרד הבינוי והשיכון"
AuthorityID_table['19'] = "נציגות קונסולרית ישראלית בחוץ לארץ"
AuthorityID_table['21'] = "רשות העתיקות"
AuthorityID_table['23'] = "המנהל האזרחי"
AuthorityID_table['24'] = "מעבדת בדיקה"



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
        # print(f"MySQL Database connection successful (hostname='{host_name}', database name='{db_name}')")
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



def retrieve_sons(connection, itemId):
    query = "SELECT ID FROM CustomsItem where CustomsBookTypeID = 1 and Parent_CustomsItemID=" + itemId + ";"
    results, columns = read_query(connection, query)
    return results


def retrieve_only_leaves(connection):
    limit = 400
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
    #print(list_of_leaves[0:10])
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


def cache_parents_of_all_item_ids(connection):
    global parents_of_items_cache
    if len(parents_of_items_cache) > 0:
        return
    query = "SELECT ID, Parent_CustomsItemID FROM CustomsItem;"
    results, columns = read_query(connection, query)
    list_of_tuples = [(str(x[0]), x[1]) for x in results]
    parents_of_items_cache = dict(list_of_tuples)


def cache_full_classification_of_all_item_ids(connection):
    global full_classification_of_item_ids_cache
    global item_id_of_full_classification_cache
    if len(full_classification_of_item_ids_cache) > 0:
        return
    query = "SELECT ID, FullClassification FROM CustomsItem" + " WHERE CustomsBookTypeID = 1;"
    results, columns = read_query(connection, query)
    list_of_tuples = [(str(x[0]), x[1]) for x in results]
    full_classification_of_item_ids_cache = dict(list_of_tuples)
    item_id_of_full_classification_cache = dict([(str(x[1]), x[0]) for x in results])


def get_item_id_of_full_classification(fullClassification):
    if fullClassification in item_id_of_full_classification_cache:
        return str(item_id_of_full_classification_cache[fullClassification])
    return None


def retrieve_full_classification_of_item_ids1(connection, list_of_item_ids):
    query = "SELECT ID, FullClassification FROM CustomsItem;"
    results, columns = read_query(connection, query)
    #list_of_ids = [str(x[0]) for x in results if str(x[0]) in list_of_item_ids]  # a generator that iterates over all tuples, from each tuple takes the first value
    #list_of_full_classifications = [str(x[1]) for x in results if str(x[0]) in list_of_item_ids]  # a generator that iterates over all tuples, from each tuple takes the second value
    list_of_tuples = [x for x in results if str(x[0]) in list_of_item_ids]
    #print(list_of_ids[0:10])
    #print(list_of_full_classifications[0:10])
    print(list_of_tuples[0:10])


def retrieve_full_classification_of_item_ids(connection, list_of_item_ids):
    cache_full_classification_of_all_item_ids(connection)   # fill cache, only if needed!
    list_of_tuples = list()
    for item_id in list_of_item_ids:
        tup = tuple((item_id, full_classification_of_item_ids_cache[item_id]))
        list_of_tuples.append(tup)
    print(list_of_tuples)
    return list_of_tuples


def retrieve_parent1(connection, customs_item_id):
    query = "SELECT ID, Parent_CustomsItemID FROM CustomsItem where CustomsBookTypeID = 1 and ID = '" + customs_item_id + "';"
    results, columns = read_query(connection, query)
    # assuming only 1 row in the result!
    parent_id = results[0][1]
    #print("for item id", customs_item_id, "the parent is", parent_id)
    return parent_id


def retrieve_parent(connection, customs_item_id):
    parent_id = 0
    if customs_item_id in parents_of_items_cache:
        parent_id = parents_of_items_cache[customs_item_id]
    if parent_id is None:
        parent_id=0
    return parent_id


def list_of_full_classifications(list_of_customs_item_ids):
    list_of_fc = [full_classification_of_item_ids_cache[item_id] for item_id in list_of_customs_item_ids]
    return list_of_fc


def zipped_list_of_full_classifications(list_of_customs_item_ids):
    fcs = list_of_full_classifications(list_of_customs_item_ids)
    zipped = list(zip(list_of_customs_item_ids, fcs))
    # print(zipped)
    return zipped


def retrieve_all_parents_of_item(connection, customs_item_id):
    """
    From a customs-item, find its parent, and then its parent, etc. up to the
    item that has no parent.

    :param connection: a connection object to the SQL DB
    :param customs_item_id: id of the item (in CustomsItem table)
    :return: list of ids of item and all its parents, in order of walking up.
    """
    cache_full_classification_of_all_item_ids(connection)   # fill cache if needed
    cache_parents_of_all_item_ids(connection)               # fill cache if needed

    list_of_parents = list()
    list_of_parents.append(customs_item_id)
    idd = customs_item_id
    while True:
        parent_id = retrieve_parent(connection, idd)
        if parent_id == 0:
            break
        list_of_parents.append(str(parent_id))
        idd = str(parent_id)
    list_of_fc = list_of_full_classifications(list_of_parents)
    zipped_list = zipped_list_of_full_classifications(list_of_parents)
    #print("list of parents is", zipped_list)
    return list_of_parents, list_of_fc, zipped_list


def only_date(date1):
    """
    Calculate from a date object only the date part and return it as a string

    :param date1: the date object
    :return: a string with only the date
    """
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


def safe_authority_id(authority_id):
    if authority_id in AuthorityID_table.keys():
        return authority_id + "-" + AuthorityID_table[authority_id]
    return authority_id


def safe_conf_type(conf_type):
    if conf_type in ConfirmationTypeID_table.keys():
        return conf_type + "-" + ConfirmationTypeID_table[conf_type]
    return conf_type


def retrieve_name_of_item(connection, item_id):
    try:
        current_date = '2022-01-01'     # TODO not hard-coded
        query = "select ci.FullClassification, dh.GoodsDescription, dh.EnglishGoodsDescription " + \
                " from CustomsItem ci,CustomsItemDetailsHistory dh " + \
                "where ci.ID=dh.CustomsItemID " + \
                "and ci.CustomsBookTypeID=1 " + \
                "and dh.EntityStatusID<>4 and dh.EndDate > '" + current_date + "'" + \
                "and dh.CustomsItemID='" + item_id + "';"
        results, columns = read_query(connection, query)
        #print(columns)
        #print(results)
        # ('FullClassification', 'GoodsDescription', 'EnglishGoodsDescription')
        # [('1001190000', 'אחר', 'Other')]
        return (columns, results[0])
    except Exception as ex:
        print("Exception", ex, 'for item', item_id)
        return None


def retrieve_regularity_requirement(connection, item_id):
    """
    This method retrieves from SQL db, **for a single item-id** the data that is displayed in the part of Regulatory Requirements.
    The logic here is based on our assumptions of how the web-site pages are created from the data.
    In some edge cases it is not yet complete.
     Known Issues:
       1. How exactly does the web-site decide which rows to include in the display?
          It is according to start-date and end-date, but in some cases it is not straight-forward
       2. query is hard-coded
       3. column numbers are used, and they depend on the exact query
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
    #print(columns)
    #('ID', 'TypeID', 'Title', 'State', 'CreateDate', 'CreateUserID', 'UpDatetimeDate', 'UpDatetimeUserID', 'OrganizationUnitID', 'CustomerID', 'CountryID', 'IsAllCountries', 'CustomsItemID', 'IsAllCustomsItems', 'IsLimitedCountryRegularityRequirement', 'StartDate', 'EndDate', 'MekachDate', 'InceptionCodeID', 'RegularityPublicationCodeID19', '20RegularitySourceCodeID', 'CustomsBookTypeID', 'MekachID', 'ID', 'RegularityRequirementID', 'InterConditionsRelationshipID', 'IsPersonalImportIncluded', 'RequirementGoodsDescription', 'RegularityRequirementWarningsID', 'IsCarnetIncluded', 'ID', 'RegularityInceptionID', 'ConfirmationTypeID', 'CNumber', 'TextualCondition', 'TrNumber', 'AuthorityID')
    #0: (3962, 0, 'TEMPORARILY_NULL', 0, datetime.datetime(2011, 6, 1, 0, 0), 0, datetime.datetime(1970, 1, 1, 2, 0), 0, 0, 0, 0, 1, 26074, 0, 0, datetime.datetime(2011, 6, 1, 0, 0), datetime.datetime(2069, 12, 31, 0, 0), datetime.datetime(1970, 1, 1, 2, 0), 1, 1, 2, 1, 0, 3499, 3962, 1, 1, ' ', 0, 0, 1818, 3499, 1, 0, '', 0, 1)
    #0: (5934, 0, 'TEMPORARILY_NULL', 0, datetime.datetime(2020, 3, 25, 0, 0), 0, datetime.datetime(1970, 1, 1, 2, 0), 0, 0, 0, 0, 1, 26074, 0, 0, datetime.datetime(2011, 6, 1, 0, 0), datetime.datetime(2069, 12, 31, 0, 0), datetime.datetime(1970, 1, 1, 2, 0), 1, 20, 2, 1, 0, 7108, 5934, 1, 1, ' ', 0, 0, 10310, 7108, 1, 0, '', 0, 1)

    cache_full_classification_of_all_item_ids(connection)   # fill cache if needed

    counter = 0
    reqs = list()
    for row in results:
        # המקור החוקי לדרישה
        # 'RegularityPublicationCodeID': '1'  is Tosefet 2 LeZav Yevu Hofshi תוספת 2 לצו יבוא חופשי
        # 3  "Hakika Acheret LeZav Matan Rishyonot Yevu" חקיקה אחרת לצו מתן רשיונות יבוא
        # 'RegularityPublicationCodeID': '7' is "Ishur Mancal LeTaarif Meches" אישור מנכל לתעריף מכס
        # RegularityPublicationCodeID    '16' is "Hakika Acheret LeZav Aluf"     חקיקה אחרת לצו אלוף
        # 'RegularityPublicationCodeID': '20' is Tosefet 2 LeZav Yevu Ishi!!!   תוספת 2 לצו יבוא אישי
        #print(str(counter), ":",row)
        d = dict()
        d['order'] = counter
        # column numbers below depend on the exact query hard-coded above!
        d['RegularityRequirementID'] = str(row[0])
        d['from_item'] = item_id
        d['from_item_fc'] = full_classification_of_item_ids_cache[item_id]
        d['create_date'] = only_date(row[4])
        d['update_date'] = only_date(row[6])
        d['start_date'] = only_date(row[15])
        d['end_date'] = only_date(row[16])
        d['InceptionCodeID'] = str(row[18])
        d['RegularityPublicationCodeID'] = str(row[19])     # מקור חוקי לדרישה  see comment above!!
        #'20RegularitySourceCodeID', 'CustomsBookTypeID', 'MekachID', 'ID', 'RegularityRequirementID', 'InterConditionsRelationshipID', 'IsPersonalImportIncluded', 'RequirementGoodsDescription', 'RegularityRequirementWarningsID', 'IsCarnetIncluded',
        # '30ID', 'RegularityInceptionID', 'ConfirmationTypeID', 'CNumber', 'TextualCondition', 'TrNumber', 'AuthorityID')
        d['RegularityInceptionID'] = str(row[23])
        d['InterConditions'] = str(row[25])     # יחס תנאים
        if d['InterConditions']=='1':
            d['InterConditions']='1-All'
        if d['InterConditions'] == '2':
            d['InterConditions']='2-Tnay Yachid'
        elif d['InterConditions']=='3':
            d['InterConditions']='3-Alt'    # חליפי
        d['personal'] = str(row[26])    #1=Yes, 0=No    # חל ביבוא אישי
        if d['personal']=='1':
            d['personal']='1-Yes'
        elif d['personal']=='0':
            d['personal']='0-No'
        d['description'] = str(row[27])
        d['RegularityRequiredCertificateID'] = str(row[30])
        # ConfirmationTypeID (together with AuthorityID?): see ConfirmationTypeID_table and comments at beginning of file
        d['ConfirmationTypeID'] = safe_conf_type(str(row[32]))     # סוג אישור
        d['CNumber'] = str(row[33])
        d['TextualCondition'] = str(row[34])    # תיאור תנאים
        d['TrNumber'] = str(row[35])    # תיאור תנאים
        d['AuthorityID'] = safe_authority_id(str(row[36])) # see AuthorityID_table and comments at beginning of file
        # append only lines in which current date is between d['start_date'] and d['end_date'] = only_date(row[16])
        #reqs.append(d)
        if current_date>d['start_date'] and current_date<d['end_date']:
            reqs.append(d)
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


def print_flattened_list(lis):
    for item in lis:
        print(item)


def retrieve_for_all_parents(connection, item_id):
    """
    This method retrieves from SQL db, the whole data that is displayed in the part of Regulatory Requirements.
    It does the walking from item-id to all its parents.
    item-id is assumed to be a leaf
    """
    # fill caches from DB
    cache_full_classification_of_all_item_ids(connection)
    cache_parents_of_all_item_ids(connection)

    list_of_parents, fcs, zipped = retrieve_all_parents_of_item(connection, item_id)
    all_reqs = list()
    for item in list_of_parents:
        reqs = retrieve_regularity_requirement(connection, item)
        if len(reqs) == 0:
            continue
        all_reqs.append(reqs)
    # now flatten the list of lists
    flattened_list = list(chain.from_iterable(all_reqs))
    #print('===============')
    #print(zipped)
    #print_flattened_list(flattened_list)
    return flattened_list


def unknown_confirmation_type():
    global known_confirmation_id
    global all_conf_ids
    known = set(known_confirmation_id)
    all = set(all_conf_ids)
    unknown_conf_ids = all.difference(known)
    str_unknown_conf_ids = [str(x) for x in unknown_conf_ids]
    return str_unknown_conf_ids


def find_all_confirmation_ids(connection):
    query = "SELECT ID, ConfirmationTypeID FROM RegularityRequiredCertificate;"
    results, columns = read_query(connection, query)
    all_ids = set()
    for row in results:
        all_ids.add(row[1])
    print(sorted(all_ids))


def searchConfirmationTypeIDs(connection):
    find_all_confirmation_ids(connection)
    unknown_conf_ids = unknown_confirmation_type()
    list_of_leave_ids = retrieve_only_leaves(connection)
    set_found_conf_ids = set()
    counter = 0
    print("searching all", len(list_of_leave_ids), "leaf items...")
    for item in list_of_leave_ids:
        counter = counter + 1
        if counter % 100 == 0:
            print(counter)
        list_of_regulations = retrieve_for_all_parents(connection, item)
        for reg in list_of_regulations:
            conf_id = reg['ConfirmationTypeID']
            if conf_id in unknown_conf_ids:
                set_found_conf_ids.add(conf_id)
                print(item)
                print(reg)
        # print(list_of_regulations[0])


def initialize_connection_and_caches():
    connection = connect()
    if connection is None:
        exit(-1)
    # fill caches from DB
    cache_full_classification_of_all_item_ids(connection)
    cache_parents_of_all_item_ids(connection)
    return connection


def do_some_queries():
    connection = connect()
    if connection is None:
        exit(-1)
    # fill caches from DB
    cache_full_classification_of_all_item_ids(connection)
    cache_parents_of_all_item_ids(connection)
    #retrieve_customs_item_by_full_classification(connection, '4823691000')
    #retrieve_some_data_of_customs_item(connection, 'XV')
    #retrieve_parent_items_of_customs_item(connection, '4823691000')
    #retrieve_customs_item_by_full_classification(connection, 'XV')
    #retrieve_all_import_Full_Classifications_as_sorted_list(connection)
    #list_of_parents = retrieve_all_parents_of_item(connection, '16')
    #print(list_of_parents)
    #list_of_leave_ids = retrieve_only_leaves(connection)
    #list_of_leave_ids.insert(0, '25783')
    # retrieve_full_classification_of_item_ids(connection, list_of_ids)
    list_of_ids = retrieve_only_leaves(connection)
    for item in list_of_ids:
        retrieve_for_all_parents(connection, item)


def main():
    # do_simple_query()
    # do_dataframe_query()
    # do_some_queries()
    # list_of_parents= retrieve_all_parents_of_item(connect(), '4')
    #df = retrieve_customs_item_by_full_classification(connect(), '1509903200')
    list_of_regulations = retrieve_for_all_parents(connect(), '32739')
#32739 - some exception: KeyError: '32739' - it has no parents and no FullClassification (should be 1509903200)
# probably this is because DB is not up-to-date?



if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
