#
# more Python code to process data in Excel file and plot graphs
#
#


import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import datetime
from ast import literal_eval

from readWriteExcelFile import read_existing_results_file


"""
Create plots of various calculations. We use Pandas and Matplotlib on the Excel file.

see comment at module plotGraphs.py.

"""

NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA = "all_the_customs_items.xlsx"

COLUMN_NAME_NUMBER_OF_ISHURIM = "Number_Of_Ishurim"
COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM = "Number_Of_Gormim"
COLUMN_NAME_NUMBER_OF_IMPORTERS = "Number_Of_Importers"
COLUMN_NAME_NUMBER_OF_AGENTS = "Number_Of_Agents"
COLUMN_NAME_NUMBER_OF_DECLARATIONS = "Number_Of_Declarations"
COLUMN_NAME_ISHURIM_LIST = "Regulations"
COLUMN_NAME_GORMIM_MEASHRIM_LIST = "Confirmers"


def check_if_df_contains_data_to_plot(df):
    if COLUMN_NAME_NUMBER_OF_ISHURIM in df:
        return True
    return False


def add_count_ishurim(file_df):
    """
    add values in the columns COLUMN_NAME_NUMBER_OF_ISHURIM, COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM
    :param file_df:
    :return:
    """
    for ind in file_df.index:
        list_of_regulations_as_str = file_df.at[ind, COLUMN_NAME_ISHURIM_LIST]
        v = literal_eval(list_of_regulations_as_str)
        file_df.at[ind, COLUMN_NAME_NUMBER_OF_ISHURIM] = len(v)
        list_of_gormim_as_str = file_df.at[ind, 'Confirmers']
        v2 = literal_eval(list_of_gormim_as_str)
        file_df.at[ind, COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM] = len(v2)


def calculate_dataframe():
    file_df = read_existing_results_file(NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA)
    add_count_ishurim(file_df)
    if not check_if_df_contains_data_to_plot(file_df):
        print("===> Error: File does not contain required data")
        return
    condition_scraped_lines = file_df[COLUMN_NAME_NUMBER_OF_ISHURIM].notnull()
    df = file_df[condition_scraped_lines]
    return df


def plot_bar_of_number_of_gormim(df):
    x2 = df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM].value_counts()
    p1 = plt.bar(x2.index, df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM].value_counts())
    # for a horizintal bar graph, use barh:
    # plt.barh(x.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts())
    ss = "(םיטירפ " + str(df.shape[0]) + " כהס) "
    ss2 = "מספר הפריטים שעבורם נדרש מספר גורמים מאשרים "
    title = ss+ss2[::-1]
    plt.title(title)  # "Number of Ishurim")

#    plt.ylabel('Number of items')
    plt.ylabel("מספר פריטי מכס"[::-1])
    plt.xlabel('מספר גורמים מאשרים'[::-1])
    plt.show()


def allRegulationCodesInFile(df):
    """
    Find all the regulation codes ('0101', '0102', etc) that exist in the dataframe
    in any of the lists in column COLUMN_NAME_ISHURIM_LIST
    :param df: dataframe containing content of the Excel file
    :return: sorted list of all regulation codes found in the dataframe ('0101', '0102', etc)
    """
    all_codes = set()
    for ind in df.index:
        list_of_regulations_as_str = df.at[ind, COLUMN_NAME_ISHURIM_LIST]
        v = literal_eval(list_of_regulations_as_str)
        for code in v:
            all_codes.add(code)
    result = sorted(all_codes, reverse=True)
    print(result)
    return result


def howManyItemsHaveEachRegulationCode(onlyItemsWithDeclarations = False):
    file_df = read_existing_results_file(NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA)
    all_codes = allRegulationCodesInFile(file_df)
    regulations = sorted(all_codes)
    # results = []
    # for reg in regulations:  #  regulations:
    #     results.append(howManyItemsHaveThisSpecificRegulation(file_df, reg, onlyItemsWithDeclarations))
    #same_calc_using_list_comprehension:
    results = [howManyItemsHaveThisSpecificRegulation(file_df, reg, onlyItemsWithDeclarations) for reg in regulations]
    return regulations, results


# def howManyItemsHaveRegulation2(regulations):
#     file_df = read_existing_results_file(NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA)   # no need to count ishurim
#     results = []
#     for reg in regulations:
#         results.append(howManyItemsHaveThisSpecificRegulation(file_df, reg))
#     return results


def howManyItemsHaveThisSpecificRegulation(df, regulation_code, include_only_items_with_declarations = False):
    """
    Count number of items in the dataframe that have the specified regulation code in their list of codes in column COLUMN_NAME_ISHURIM_LIST
    in the dataframe, column COLUMN_NAME_ISHURIM_LIST contains a list (as String!)
    of the regulations required for this item.
    :param df: DataFrame containing the data (usually read from Excel file)
    :param regulation_code: the code of Ishur, such as '0102'
    :param include_only_items_with_declarations: True/False whether to count also customs-items without data about number of declarations
    :return: a Number - number of items in the dataframe that have the specified regulation code in their list of codes in column COLUMN_NAME_ISHURIM_LIST
    """
    df["code"] = ''     # add a column named "code" to the DataFrame
    for ind in df.index:
        list_of_regulations_as_str = df.at[ind, COLUMN_NAME_ISHURIM_LIST]
        list_of_codes = literal_eval(list_of_regulations_as_str)
        # column COLUMN_NAME_ISHURIM_LIST in the DataFrame contains this list_of_codes,
        # Now in each cell in column "code" we put True or False according to - if given regulation is in the list of codes
        df.at[ind, "code"] = regulation_code in list_of_codes

    # filter the df to retain only lines containing value True in column named "code"
    # (and possibly only if they have a number > 0 in column COLUMN_NAME_NUMBER_OF_DECLARATIONS)
    condition = df["code"] == True
    if include_only_items_with_declarations:
        condition = (df["code"] == True) & (df[COLUMN_NAME_NUMBER_OF_DECLARATIONS]>0)
    df2 = df[condition]     # <-- this is the filtered dataframe

    # count how many lines in the dataframe
    howMany = df2.shape[0]

    return howMany


def howManyCustomsItemsNeedEachRegulation(onlyItemsWithDeclarations = False):
    codes, counts = howManyItemsHaveEachRegulationCode(onlyItemsWithDeclarations)
    #print("codes", codes, " - counted", counts, "items")
    counts_dict = as_dictionary = dict(zip(codes[:-6], counts[:-6]))    # for convenience I remove last 6 codes because they are Hebrew text
    print(counts_dict)
    return counts_dict


def calc_how_many():
    d1 = howManyCustomsItemsNeedEachRegulation()
#                   {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4, '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4, '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54, '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70, '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583, '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143, '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98, '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    d2 = howManyCustomsItemsNeedEachRegulation(True)
# declarations>0    {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4, '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4, '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51, '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57, '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500, '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122, '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87, '2101': 3, '2301': 277, '2303': 252, '2402': 1713}



def do_some_plotting2():
    """
    Some other plotting possibilities
    :return: nothing
    """
    d1 = howManyCustomsItemsNeedEachRegulation()
    series1 = pd.Series(d1)
    #                   {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4, '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4, '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54, '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70, '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583, '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143, '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98, '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    d2 = howManyCustomsItemsNeedEachRegulation(True)
    series2 = pd.Series(d2)
    # declarations>0    {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4, '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4, '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51, '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57, '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500, '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122, '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87, '2101': 3, '2301': 277, '2303': 252, '2402': 1713}

    p1 = plt.barh(series1.index[:8], series1.values[:8])
    p2 = plt.barh(series2.index[:8], series2.values[:8])
    plt.title("כמה פריטי מכס צריכים אישור זה"[::-1])
    plt.ylabel("קוד אישור"[::-1])
    plt.xlabel("מספר פריטי מכס הזקוקים לאישור זה"[::-1])
    plt.show()

    p3 = plt.barh(series1.index[8:23], series1.values[8:23])
    p4 = plt.barh(series2.index[8:23], series2.values[8:23])
    plt.show()

    p5 = plt.barh(series1.index[23:34], series1.values[23:34])
    p6 = plt.barh(series2.index[23:34], series2.values[23:34])
    plt.show()




def test_count_items_that_need_regulation():
    """
    Test function to see if counting from Excel gives the correct results.
    This of course assumes that the solution hard-coded below is the correct solution.
    :return: nothing (prints to console)
    """
    counted_in_excel_file = howManyCustomsItemsNeedEachRegulation()
    expected_solution = {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4, '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4, '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54, '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70, '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583, '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143, '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98, '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    if counted_in_excel_file == expected_solution:
        print("<== count OK")
    else:
        print("<== count NOT SAME!!")


def test_count_items_that_need_regulation2():
    """
    Test function to see if counting from Excel gives the correct results.
    This of course assumes that the solution hard-coded below is the correct solution.
    :return: nothing (prints to console)
    """
    counted_in_excel_file = howManyCustomsItemsNeedEachRegulation(True)
    expected_solution = {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4, '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4, '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51, '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57, '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500, '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122, '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87, '2101': 3, '2301': 277, '2303': 252, '2402': 1713}
    if counted_in_excel_file == expected_solution:
        print("<== count OK")
    else:
        print("<== count NOT SAME!!")


def do_some_plotting():
    """
    Some other plotting possibilities
    :return: nothing
    """
    #d1 = howManyCustomsItemsNeedEachRegulation()
    d1 = {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4, '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4, '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54, '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70, '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583, '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143, '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98, '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    series1 = pd.Series(d1)
    #d2 = howManyCustomsItemsNeedEachRegulation(True)
    d2 = {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4, '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4, '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51, '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57, '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500, '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122, '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87, '2101': 3, '2301': 277, '2303': 252, '2402': 1713}
    series2 = pd.Series(d2)

    def add_titles(plt):
        plt.title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=12, fontweight='bold')
        plt.ylabel("קוד אישור"[::-1], fontsize=12, fontweight='bold', )
        plt.xlabel("מספר פריטי מכס הזקוקים לאישור זה"[::-1])
        # plt.tick_params(axis='x', labelsize=15, rotation=90)
        plt.legend()

    def show_plot(plt, series1, series2, xmin, xmax):
        pp1 = plt.barh(series1.index[xmin:xmax], series1.values[xmin:xmax],
                       label='כולל ללא הצהרות יבוא'[::-1])  # , height=0.9)
        pp2 = plt.barh(series2.index[xmin:xmax], series2.values[xmin:xmax],
                       label='רק עם הצהרות יבוא'[::-1])  # , color='g', height=0.9)
        add_titles(plt)
        plt.show()

    show_plot(plt, series1, series2, 0, 8)
    show_plot(plt, series1, series2, 8, 23)
    show_plot(plt, series1, series2, 23, 34)
    show_plot(plt, series1, series2, 34, 39)
    show_plot(plt, series1, series2, 39, 50)
    show_plot(plt, series1, series2, 50, 61)

    plt.show()




def do_plot_customs_items_requiring_each_regulation(calculate_from_excel_file = False):
    # These are hard coded results - instead of doing the calculation on the Excel file (each calculation takes ~10 seconds)
    d1 = {'0101': 214, '0102': 219, '0103': 2, '0104': 1547, '0105': 1, '0107': 13, '0109': 37, '0110': 4, '0201': 261, '0202': 15, '0203': 6, '0204': 401, '0209': 147, '0210': 81, '0212': 124, '0213': 4, '0214': 11, '0215': 124, '0217': 39, '0218': 20, '0219': 1509, '0221': 16, '0222': 21, '0302': 54, '0303': 15, '0305': 36, '0307': 5, '0308': 324, '0309': 3, '0310': 49, '0311': 231, '0315': 70, '0319': 457, '0325': 1884, '0402': 1886, '0501': 1, '0602': 24, '0603': 35, '0604': 11, '0701': 583, '0702': 284, '0703': 99, '0704': 164, '0705': 582, '0706': 30, '0708': 15, '0709': 6, '0710': 143, '0713': 1, '0715': 11, '0804': 9, '1001': 18, '1101': 11, '1201': 3, '1203': 21, '1204': 1, '1301': 98, '2101': 3, '2301': 311, '2303': 281, '2402': 1883}
    d2 = {'0101': 181, '0102': 189, '0103': 2, '0104': 1405, '0105': 1, '0107': 12, '0109': 28, '0110': 4, '0201': 234, '0202': 14, '0203': 2, '0204': 373, '0209': 130, '0210': 64, '0212': 120, '0213': 4, '0214': 11, '0215': 92, '0217': 32, '0218': 16, '0219': 1373, '0221': 9, '0222': 14, '0302': 51, '0303': 10, '0305': 35, '0307': 5, '0308': 277, '0309': 3, '0310': 45, '0311': 186, '0315': 57, '0319': 387, '0325': 1714, '0402': 1716, '0501': 0, '0602': 19, '0603': 28, '0604': 10, '0701': 500, '0702': 248, '0703': 97, '0704': 140, '0705': 499, '0706': 29, '0708': 15, '0709': 4, '0710': 122, '0713': 1, '0715': 10, '0804': 9, '1001': 17, '1101': 2, '1201': 3, '1203': 17, '1204': 0, '1301': 87, '2101': 3, '2301': 277, '2303': 252, '2402': 1713}
    if calculate_from_excel_file:
        d1 = howManyCustomsItemsNeedEachRegulation()
        d2 = howManyCustomsItemsNeedEachRegulation(True)

    plt.figure(figsize=[20, 7])
    pl=plt.bar(d1.keys(), d1.values(), width=0.5, linewidth=2, label = "כולל ללא הצהרות יבוא"[::-1]
            #color=col_map.colors, edgecolor='maroon',
            )
    index = 0
    for bar in pl:
        x_code = list(d1.keys())[index]
        description_value = bar.get_height()    # if we want description of each bar to be total number of such items
        percent = 100*d2[x_code]/d1[x_code]
        description_value = str(int(percent)) + "%"     # if we want description of each bar to be percent of count without 0 number of declarations from count with any number
        plt.annotate(description_value, xy=(bar.get_x() - 0.07, bar.get_height() + 10), fontsize=8)
        index = index + 1

    pl2 = plt.bar(d2.keys(), d2.values(), width=0.7, label="רק עם הצהרות יבוא"[::-1])
    plt.title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=15)
    plt.xlabel('קוד אישור'[::-1], fontsize=15)
    plt.ylabel('מספר פריטים'[::-1], fontsize=15)
    plt.xticks(fontsize=10, rotation=90)
    plt.legend()
    plt.show()


def main():
    # do_some_plotting()
    plot_bar_of_number_of_gormim(calculate_dataframe())
    do_plot_customs_items_requiring_each_regulation()


def test():
    test_count_items_that_need_regulation()
    test_count_items_that_need_regulation2()


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    # test()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
