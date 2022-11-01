import datetime
import math

from ast import literal_eval

import readDB
import readWriteExcelFile
import translationTables
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


def find_name_for_specific_item(fullClass, flattened_list, do_print = False):
    for data in flattened_list:
        print(data)


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


def find_names():
    connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file("all_the_customs_items.xlsx")
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        flattened_list = readDB.retrieve_for_all_parents(connection, item_id)
        find_name_for_specific_item(fullClass, flattened_list)


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


def add_Tkanim_columns(file_name):
    COLUMN_NAME = 'Tkanim'
    if file_name is None or len(file_name)==0:
        return None
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    df = existingDF.copy()
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        if isinstance(val_as_str, float) and math.isnan(val_as_str):
            continue
        val_as_list = literal_eval(val_as_str)
        number_of_tkanim = len(val_as_list)
        for teken_column_num in range(number_of_tkanim):
            the_Teken = val_as_list[teken_column_num]
            name_of_column = 'Teken_' + str(teken_column_num+1)     # column names will be Teken_1, Teken_2, ...
            if name_of_column not in df.columns:
                # add a new colum with that name
                print('adding column', name_of_column)
                df[name_of_column] = ''
            if name_of_column in df.columns:
                # column already exists
                df.at[fullClass, name_of_column] = the_Teken
            else:
                print('===> impossible: column', name_of_column, 'not found after it was added')
    return df


def add_regulations_columns(file_name):
    COLUMN_NAME = 'Regulations'
    if file_name is None or len(file_name)==0:
        return None
    # connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    df = existingDF.copy()
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        val_as_list = literal_eval(val_as_str)
        for reg_code in val_as_list:
            heb_val = translationTables.regulation_from_code(reg_code)
            if heb_val not in df.columns:
                # add a new colum with that name
                print('adding column', heb_val)
                df[heb_val] = ''
            if heb_val in df.columns:
                # column already exists
                df.at[fullClass, heb_val] = 'Yes'
            else:
                print('===> impossible: column', heb_val, 'not found after it was added')
    print(df)
    return df


def add_confirmers(file_name):
    COLUMN_NAME = 'Confirmers'
    if file_name is None or len(file_name)==0:
        return None
    # connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    df = existingDF.copy()
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        val_as_list = literal_eval(val_as_str)
        for confirmer_code in val_as_list:
            heb_val = translationTables.confirmer_from_code(confirmer_code)
            if heb_val not in df.columns:
                # add a new colum with that name
                print('adding column', heb_val)
                df[heb_val] = ''
            if heb_val in df.columns:
                # column already exists
                df.at[fullClass, heb_val] = 'Yes'
            else:
                print('===> impossible: column', heb_val, 'not found after it was added')
    print(df)
    return df


def add_regulations_as_text(file_name):
    COLUMN_NAME = 'Regulations'
    NEW_COLUMN_NAME = 'Regulations_Heb'
    if file_name is None or len(file_name)==0:
        return None
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    df = existingDF.copy()
    df[NEW_COLUMN_NAME] = ''
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        val_as_list = literal_eval(val_as_str)
        list_as_heb_text = []
        for regulation_code in val_as_list:
            heb_val = translationTables.regulation_from_code(regulation_code)
            list_as_heb_text.append(heb_val)
        df.at[fullClass, NEW_COLUMN_NAME] = list_as_heb_text
    return df


def add_confirmers_as_text(file_name):
    COLUMN_NAME = 'Confirmers'
    NEW_COLUMN_NAME = 'Confirmers_Heb'
    if file_name is None or len(file_name)==0:
        return None
    existingDF = read_existing_results_file(file_name)
    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    df = existingDF.copy()
    df[NEW_COLUMN_NAME] = ''
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        val_as_list = literal_eval(val_as_str)
        list_as_heb_text = []
        for confirmer_code in val_as_list:
            heb_val = translationTables.confirmer_from_code(confirmer_code)
            list_as_heb_text.append(heb_val)
        df.at[fullClass, NEW_COLUMN_NAME] = list_as_heb_text
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
    for fullClass in customsItemFullClassificationList:
        #print(fullClass)
        item_id = readDB.get_item_id_of_full_classification(fullClass)
        if item_id is None:
            continue
        item_count = item_count + 1
        res = readDB.retrieve_name_of_item(connection, item_id)



def write_df_to_new_file(new_file_name, newDF):
    if newDF is None:  # dataFrame was not built correctly
        exit(-2)
    write_to_excel_file2(new_file_name, newDF)


def add_tkanim_and_write_to_file(source_file = 'all_the_customs_items.xlsx', dest_file = 'newfile.xlsx'):
    df = add_tkanim_to_existing_df(source_file)
    write_df_to_new_file(dest_file, df)


def add_names_and_write_to_file(source_file='all_with_tkanim.xlsx', dest_file = 'newfile.xlsx'):
    df = add_item_description_names_to_existing_df(source_file)
    write_df_to_new_file(dest_file, df)


def count_values_in_column(file_name):
    '''
        example: count_values_in_column('all_with_tkanim_and_names.xlsx')
    :param file_name:
    :return:
    '''
    COLUMN_NAMEs = ['Confirmers', 'Regulations', 'Tkanim' ]    # all_with_tkanim_and_names.xlsx

    if file_name is None or len(file_name) == 0:
        return None
    # connection = initialize_connection_and_caches()
    existingDF = read_existing_results_file(file_name)
    for col_name in COLUMN_NAMEs:
        count_values_in_column_in_existing_df(existingDF, col_name, sort_numeric=col_name in ['Confirmers', 'Tkanim' ])


def count_values_in_column_in_existing_df(existingDF, COLUMN_NAME, sort_numeric = False):
    list_of_vals = []

    customsItemFullClassificationList = extractCustomItemsAsList(existingDF)
    for fullClass in customsItemFullClassificationList:
        val_as_str = existingDF.at[fullClass, COLUMN_NAME]
        if isinstance(val_as_str, float) and math.isnan(val_as_str):
            continue
        try:
            val = literal_eval(val_as_str)      # convert the string "['0', '1']" to a list of 2 items!!
        except ValueError:
            print('===> ERROR with: ', val_as_str)
        if val is not None and len(val) > 0:
            list_of_vals.extend(val)
            list_of_vals = remove_duplicates(list_of_vals)
            # print(list_of_vals)
    # sort list_of_vals in-place by numeric value
    if sort_numeric:
        list_of_vals.sort(key=int)
    else:
        list_of_vals.sort()

    print(COLUMN_NAME, ":", list_of_vals)


def add_confirmers_as_colums(source_file='all_with_tkanim_and_names.xlsx', dest_file='newfile.xlsx'):
    df = add_confirmers(source_file)
    write_df_to_new_file(dest_file, df)


def add_tkanim_as_columns(source_file='all_with_regulations_columns.xlsx', dest_file='newfile.xlsx'):
    df = add_Tkanim_columns(source_file)
    write_df_to_new_file(dest_file, df)


def add_regulations_as_colums(source_file='all_with_confirmers_columns.xlsx', dest_file='newfile.xlsx'):
    df = add_regulations_columns(source_file)
    write_df_to_new_file(dest_file, df)


def add_confirmers_as_hebrew_list(source_file='all_with_tkanim_and_names.xlsx', dest_file='newfile.xlsx'):
    df = add_confirmers_as_text(source_file)
    write_df_to_new_file(dest_file, df)


def add_regulations_as_hebrew_list(source_file='all_with_conf_heb.xlsx', dest_file='newfile.xlsx'):
    df = add_regulations_as_text(source_file)
    write_df_to_new_file(dest_file, df)


def main():
    add_tkanim_and_write_to_file(source_file='all_the_customs_items.xlsx', dest_file='01.xlsx')
    add_names_and_write_to_file(source_file='01.xlsx', dest_file='02.xlsx')
    add_confirmers_as_hebrew_list(source_file='02.xlsx', dest_file='03.xlsx')
    add_regulations_as_hebrew_list(source_file='03.xlsx', dest_file='04.xlsx')
    add_confirmers_as_colums(source_file='04.xlsx', dest_file='05.xlsx')
    add_regulations_as_colums(source_file='05.xlsx', dest_file='06.xlsx')
    add_tkanim_as_columns(source_file='06.xlsx', dest_file='07.xlsx')


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    try:
        main()
    finally:
        print('started at', startedAt)
        print('completed at', datetime.datetime.now())


'''
Confirmers : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '19', '21', '23', '24']
Tkanim : ['-1', '1', '5', '6', '20', '23', '27', '32', '33', '37', '47', '61', '62', '66', '69', '70', '80', '87', '89', '90', '100', '103', '107', '129', '139', '145', '158', '169', '172', '211', '215', '221', '222', '240', '255', '261', '272', '282', '283', '299', '314', '318', '327', '365', '371', '383', '386', '388', '426', '428', '438', '448', '463', '472', '473', '484', '489', '520', '532', '538', '562', '565', '570', '576', '579', '597', '636', '637', '681', '682', '742', '750', '751', '764', '790', '798', '808', '818', '821', '832', '840', '844', '867', '873', '884', '885', '887', '900', '907', '915', '938', '950', '958', '968', '987', '990', '994', '995', '997', '1001', '1003', '1011', '1038', '1049', '1076', '1078', '1084', '1112', '1116', '1117', '1121', '1139', '1144', '1147', '1148', '1153', '1157', '1212', '1220', '1228', '1240', '1258', '1268', '1273', '1279', '1284', '1296', '1313', '1317', '1338', '1339', '1340', '1343', '1347', '1353', '1366', '1368', '1381', '1417', '1419', '1430', '1458', '1481', '1490', '1498', '1505', '1516', '1546', '1548', '1554', '1604', '1605', '1607', '1613', '1735', '1836', '1847', '1888', '1898', '1913', '1921', '1941', '1964', '2206', '2217', '2250', '2251', '2252', '2302', '2481', '4004', '4007', '4272', '4280', '4295', '4314', '4373', '4402', '4451', '4466', '4476', '4501', '5111', '5113', '5115', '5201', '5327', '5378', '5381', '5418', '5433', '5434', '5438', '5484', '5485', '5563', '5678', '5694', '5697', '5731', '5817', '5840', '5937', '6558', '8871', '8872', '8873', '9809', '12402', '12586', '14304', '14372', '14765', '14988', '21003', '50464', '50541', '60034', '60065', '60095', '60155', '60188', '60192', '60227', '60238', '60245', '60247', '60269', '60320', '60400', '60432', '60601', '60745', '60898', '60921', '60923', '60950', '60968', '60974', '60998', '60999', '61008', '61009', '61095', '61196', '61242', '61347', '61386', '61439', '61558', '62040', '62368', '602454', '615558']
Regulations : ['0101', '0102', '0103', '0104', '0105', '0107', '0109', '0110', '0201', '0202', '0203', '0204', '0209', '0210', '0212', '0213', '0214', '0215', '0217', '0218', '0219', '0221', '0222', '0302', '0303', '0305', '0307', '0308', '0309', '0310', '0311', '0315', '0319', '0325', '0402', '0501', '0602', '0603', '0604', '0701', '0702', '0703', '0704', '0705', '0706', '0708', '0709', '0710', '0713', '0715', '0804', '1001', '1101', '1201', '1203', '1204', '1301', '2101', '2301', '2303', '2402', 'אישור אגף ניהול משאבי תשתיות', 'אישור יצוא שירותים להגנת הצומח', 'אישור מפמכ', 'רשיון יבוא', 'רשיון יבוא מלשכת הבריאות בנפת רמלה', 'רשיון יצוא אגף הרכב ושירותי תחזוקה ']

'''