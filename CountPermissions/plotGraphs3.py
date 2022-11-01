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


def howManyItemsHaveThisSpecificRegulation3(df1, regulation_code, onlySpecificItemsOptionsDictionaty):
    # onlySpecificItemsOptionsDictionaty is like {'declarations': False, 'agents': False, 'importers': False}
    df = addColumnWithCode(df1, regulation_code)
    # filter the df to retain only lines containing value True in column named "code"
    # (and possibly only if they have a number > 0 in column COLUMN_NAME_NUMBER_OF_DECLARATIONS)
    condition = specify_condition(df, onlySpecificItemsOptionsDictionaty)
    df2 = df[condition]  # <-- this is the filtered dataframe
    # count how many lines in the dataframe
    howMany = df2.shape[0]
    return howMany


def howManyItemsHaveEachRegulationCode2(onlySpecificItemsOptionsDictionaty):
    # {'declarations': False, 'agents': False, 'importers': False}
    file_df = read_existing_results_file(NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA)
    regulations = sorted(allRegulationCodesInFile(file_df))
    results = [howManyItemsHaveThisSpecificRegulation3(file_df, reg, onlySpecificItemsOptionsDictionaty) for reg in regulations]
    return regulations, results


def addColumnWithCode(df1, regulation_code):
    df = df1.copy()
    df["code"] = ''  # add a column named "code" to the DataFrame
    for ind in df.index:
        list_of_regulations_as_str = df.at[ind, COLUMN_NAME_ISHURIM_LIST]
        list_of_codes = literal_eval(list_of_regulations_as_str)
        # column COLUMN_NAME_ISHURIM_LIST in the DataFrame contains this list_of_codes,
        # Now in each cell in column "code" we put True or False according to - if given regulation is in the list of codes
        df.at[ind, "code"] = regulation_code in list_of_codes
    return df


def specify_condition(df, onlySpecificItemsOptionsDictionaty):
    # {'declarations': False, 'agents': False, 'importers': False}
    condition = df["code"] == True
    if onlySpecificItemsOptionsDictionaty['declarations']:
        condition = (df["code"] == True) & (df[COLUMN_NAME_NUMBER_OF_DECLARATIONS] > 0)
    if onlySpecificItemsOptionsDictionaty['agents']:
        condition = (df["code"] == True) & (df[COLUMN_NAME_NUMBER_OF_AGENTS] > 0)
    if onlySpecificItemsOptionsDictionaty['importers']:
        condition = (df["code"] == True) & (df[COLUMN_NAME_NUMBER_OF_IMPORTERS] > 0)
    return condition


def howManyCustomsItemsNeedEachRegulation2(onlySpecificItemsOptionsDictionaty):
    # {'declarations': False, 'agents': False, 'importers': False}
    codes, counts = howManyItemsHaveEachRegulationCode2(onlySpecificItemsOptionsDictionaty)
    #print("codes", codes, " - counted", counts, "items")
    counts_dict = dict(zip(codes[:-6], counts[:-6]))    # for convenience I remove last 6 codes because they are Hebrew text
    print(counts_dict)
    return counts_dict


def plot_these_data(d1, d2, legend_str_without, legend_str_with, use_percents = True):
    plt.figure(figsize=[20, 7])
    pl = plt.bar(d1.keys(), d1.values(), width=0.5, linewidth=2, label=legend_str_without[::-1])
    index = 0
    for bar in pl:
        x_code = list(d1.keys())[index]
        description_value = bar.get_height()  # if we want description of each bar to be total number of such items
        if use_percents:
            percent = 100 * d2[x_code] / d1[x_code]
            description_value = str(int(percent)) + "%"  # if we want description of each bar to be percent of count without 0 number of declarations from count with any number
        plt.annotate(description_value, xy=(bar.get_x() - 0.07, bar.get_height() + 10), fontsize=8)
        index = index + 1

    pl2 = plt.bar(d2.keys(), d2.values(), width=0.7, label=legend_str_with[::-1])
    plt.title("כמה פריטי מכס צריכים אישור זה"[::-1], fontsize=15)
    plt.xlabel('קוד אישור'[::-1], fontsize=15)
    plt.ylabel('מספר פריטים'[::-1], fontsize=15)
    plt.xticks(fontsize=10, rotation=90)
    plt.legend()
    plt.show()


def do_plot_customs_items_requiring_each_regulation_for_declarations(calculate_from_excel_file = True, use_percents = True):
    d1 = {}
    d2 = {}
    if calculate_from_excel_file:
        d1 = howManyCustomsItemsNeedEachRegulation2({'declarations': False, 'agents': False, 'importers': False})
        d2 = howManyCustomsItemsNeedEachRegulation2({'declarations': True, 'agents': False, 'importers': False})
    legend_str_without, legend_str_with = ( "כולל ללא הצהרות יבוא", "רק עם הצהרות יבוא" )
    plot_these_data(d1, d2, legend_str_without, legend_str_with, use_percents)


def count_how_many_items_are_regulated_by_x_ministries(file_df):
    number_of_lines = file_df.shape[0]
    PROCESSED_COLUMN_NUM: int = 4  # if val is 4, the 5th column will be processed
    dict_num_of_items_for_each_num_of_confirmers = {}
    for index in range(number_of_lines):
        content = str(file_df.iat[index, PROCESSED_COLUMN_NUM])
        number_of_confirmers = 0
        if ',' in content:
            vals = content.split(sep=',')
            number_of_confirmers=len(vals)
        elif content=='[]' or content=='':
            number_of_confirmers=0
        else:
            number_of_confirmers=1
        if number_of_confirmers not in dict_num_of_items_for_each_num_of_confirmers.keys():
            dict_num_of_items_for_each_num_of_confirmers[number_of_confirmers] = 0
        curr_count = dict_num_of_items_for_each_num_of_confirmers[number_of_confirmers]
        dict_num_of_items_for_each_num_of_confirmers[number_of_confirmers] = curr_count + 1
    #print_results()
    result = dict(sorted(dict_num_of_items_for_each_num_of_confirmers.items()))
    print(result)
    return result

def main():
    #do_plot_customs_items_requiring_each_regulation_for_declarations(use_percents=False)
    # מפוקחים על ידי
    # count size of list in column 'Confirmers'
    file_df = read_existing_results_file(NAME_OF_SPECIFIC_RESULTS_FILE_WITH_ALL_DATA)
    num_of_items_for_each_auth_num = count_how_many_items_are_regulated_by_x_ministries(file_df)
    # now plot it
    plt.figure(figsize=[20, 7])
    plt.pie(num_of_items_for_each_auth_num.values(),
            labels=num_of_items_for_each_auth_num.keys(),
            explode=[0,0,0,0.1,0.1,0,0,0,0,0, 0],
            autopct='%1.1f%%')
    #plt.legend()
    plt.title("כמה משרדי ממשלה צריכים לאשר פריט זה?"[::-1], fontsize=30)
    plt.show()


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
