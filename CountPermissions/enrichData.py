import datetime

import readDB
import readWriteExcelFile
from readWriteExcelFile import read_existing_results_file, write_to_excel_file, write_to_excel_file2
from readDB import initialize_connection_and_caches, get_item_id_of_full_classification


COLUMN_NAME_CUSTOM_ITEM = readWriteExcelFile.NEW_COLUMN_NAME_CUSTOM_ITEM
COLUMN_NAME_NUMBER_OF_IMPORTERS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_IMPORTERS
COLUMN_NAME_NUMBER_OF_AGENTS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_AGENTS
COLUMN_NAME_NUMBER_OF_DECLARATIONS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_DECLARATIONS
COLUMN_NAME_EXTRACTED_AT_DATE = "extracted_at_date"


def extractCustomItemsAsList(df):
    """
    df has at least the following column: COLUMN_NAME_CUSTOM_ITEM as index!
    other columns are ignored.
    :param df:
    :return:
    """
    return df.index.values.tolist()


def remove_duplicates(list_of_numbers):
    s = set(list_of_numbers)
    return list(s)


def build_list_of_tkanim_for_specific_item(fullClass, flattened_list, do_print = False):
    list_of_teken_numbers = []
    for data in flattened_list:
        if data['TrNumber'] != '0':
            list_of_teken_numbers.append(data['TrNumber'])
    s = remove_duplicates(list_of_teken_numbers)
    if do_print:
        if len(s) > 1:
            print('for item', fullClass, 'found', len(s), 'tkanim:', s)
    return s


def count_number_of_tkanim_for_specific_item(fullClass, flattened_list, do_print = False):
    s = build_list_of_tkanim_for_specific_item(fullClass, flattened_list, do_print)
    if do_print:
        if len(s) > 1:
            print('for item', fullClass, 'found', len(s), 'tkanim:', s)
    return len(s)


def build_dict_of_Tkanim2(connection, customsItemFullClassificationList, limit = -1, do_print = False):
    dict_of_full_class_to_list_of_tkanim = {}
    item_count = 0
    for fullClass in customsItemFullClassificationList:
        item_count = item_count + 1
        if limit > 0 and item_count > limit:
            break
        # print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        flattened_list = readDB.retrieve_for_all_parents(connection, item_id)
        list_of_tkanim = build_list_of_tkanim_for_specific_item(fullClass, flattened_list)
        if len(list_of_tkanim) > 0:
            # add to dict
            dict_of_full_class_to_list_of_tkanim[fullClass] = list_of_tkanim
            if do_print:
                print(fullClass, list_of_tkanim)
    return dict_of_full_class_to_list_of_tkanim


def build_dict_of_Tkanim(do_print = False):
    '''
    This takes a long time (~7 minutes) because it goes over all the customs items in the DB.
    So it is not efficient.
    :return:
    '''
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file("all_the_customs_items.xlsx")
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    max_num = 0
    dict_of_full_class_to_list_of_tkanim = {}
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        flattened_list = readDB.retrieve_for_all_parents(connection, item_id)
        list_of_tkanim = build_list_of_tkanim_for_specific_item(fullClass, flattened_list)
        if len(list_of_tkanim) > 0:
            # add to dict
            dict_of_full_class_to_list_of_tkanim[fullClass] = list_of_tkanim
            if do_print:
                print(fullClass, list_of_tkanim)
    return dict_of_full_class_to_list_of_tkanim




def count_max_number_of_Tkanim2(do_print = False):
    dict_of_full_class_to_list_of_tkanim = build_dict_of_Tkanim(do_print)
    max_num = max(dict_of_full_class_to_list_of_tkanim.values(), key=len)
    print("max:", max_num)
    #return max_num
    # alternative way
    k_max, v_max = -1, []
    i = 0
    for key, val in dict_of_full_class_to_list_of_tkanim.items():
        if len(val) > len(v_max) or i == 0:
            k_max, v_max = key, val
        i += 1
    print("Longest key and value:", str(k_max) + ',' + str(v_max))


def count_max_number_of_Tkanim(do_print = False):
    '''
    This takes a long time because it goes over all the customs items in the DB.
    So it is not efficient.
    :return:
    '''
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file("all_the_customs_items.xlsx")
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    max_num = 0
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        flattened_list = readDB.retrieve_for_all_parents(connection, item_id)
        number_of_tkanim = count_number_of_tkanim_for_specific_item(fullClass, flattened_list)
        if (number_of_tkanim > max_num):
            max_num = number_of_tkanim
    if do_print:
        print('max number of Tkanim:', max_num)
    return max_num


def add_tkanim_to_existing_df(file_name):
    NEW_COLUMN_NAME = 'Tkanim'

    if file_name is None or len(file_name)==0:
        return None
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    tkanim_dict = build_dict_of_Tkanim2(connection, customsItemFullClassificationList)  # , limit = 5000)

    if len(tkanim_dict) == 0:
        print('no tkanim')
        return None

    # construct new df
    df = existingDF.copy()
    df[NEW_COLUMN_NAME] = ''
    for fullClass in tkanim_dict.keys():
        val_to_add = []
        if len(tkanim_dict[fullClass]) > 0:
            val_to_add = tkanim_dict[fullClass]
        df.at[fullClass, NEW_COLUMN_NAME] = val_to_add

    print(df)
    return df


def build_dict_of_hebrew_names(connection, customsItemFullClassificationList):
    dict_of_hebrew_names = {}
    dict_of_english_names = {}
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        res = readDB.retrieve_name_of_item(connection, item_id)
        if res is not None:
            #print(res)
            hebrew_name = res[1][1]
            english_name = res[1][2]
            print(fullClass, 'Heb=', hebrew_name, 'Eng=', english_name)
            dict_of_hebrew_names[fullClass] = hebrew_name
            dict_of_english_names[fullClass] = english_name
    return (dict_of_hebrew_names, dict_of_english_names)


def add_item_description_names_to_existing_df(file_name):
    HEB_NEW_COLUMN_NAME = 'Hebrew_Name'
    ENG_NEW_COLUMN_NAME = 'English_Name'

    if file_name is None or len(file_name)==0:
        return None
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    heb_names_dict, eng_names_dict = build_dict_of_hebrew_names(connection, customsItemFullClassificationList)

    if len(heb_names_dict) == 0:
        print('no Hebrew Names')
        return None

    # construct new df
    df = existingDF.copy()
    df = add_column_with_values(df, HEB_NEW_COLUMN_NAME, heb_names_dict)
    df = add_column_with_values(df, ENG_NEW_COLUMN_NAME, eng_names_dict)

    print(df)
    return df


def add_column_with_values(df, col_name, values_dict, val_of_empty = ''):
    '''
    Does not copy the df!! make sure you pass a df that was copied from an existing df!

    for lists call this func with val_of_empty = []
    :param df:
    :param col_name:
    :param values_dict:
    :return:
    '''
    df[col_name] = ''
    for fullClass in values_dict.keys():
        val_to_add = val_of_empty
        if len(values_dict[fullClass]) > 0:
            val_to_add = values_dict[fullClass]
        df.at[fullClass, col_name] = val_to_add
    return df


def doProcessing(authority, limit = 1000000000, trace_every = 10, authorityStr = None):
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file("all_the_customs_items.xlsx")
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    item_count = 0
    count = 0
    dict_of_TrNumber_to_list_of_items = {}
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        item_count = item_count + 1
        res = readDB.retrieve_name_of_item(connection, item_id)
        if res is not None:
            #print(res)
            hebrew_name = res[1][1]
            english_name = res[1][2]
            print(fullClass, 'Heb=', hebrew_name, 'Eng=', english_name)


def write_df_to_new_file(new_file_name, newDF):
    if newDF is None:  # dataFrame was not built correctly
        exit(-2)
    write_to_excel_file2(new_file_name, newDF)


def add_tkanim_and_write_to_file():
    df = add_tkanim_to_existing_df("all_the_customs_items.xlsx")
    write_df_to_new_file("newfile.xlsx", df)


def add_names_and_write_to_file():
    df = add_item_description_names_to_existing_df('all_with_tkanim.xlsx')
    write_df_to_new_file("newfile.xlsx", df)


def main():
    # doProcessing(7, limit = 1000, trace_every=10, authorityStr = 'Misrad HaCalcala')
    #max_count = count_max_number_of_Tkanim2(do_print=True)
    #find_names()
    add_names_and_write_to_file()


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    try:
        main()
    finally:
        print('started at', startedAt)
        print('completed at', datetime.datetime.now())
