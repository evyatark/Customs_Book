#
# Python code to process data in Excel file and plot graphs
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

Pandas is used to read data from the Excel file into a data frame,
and then do some processing of the data.
Matplotlib is used to plot graphs based on the data in the data frame.

In this module (only) we use the specific Excel file "all_the_customs_items.xlsx"!
This Excel file contains all the data read from the DB (not scraped from WebSite of Shaar Olamy!!)
This Excel file was prepared by doProcessing.py module (in this project).

Using Pandas/Matplotlib can be done either executing code in this Python file,
or by executing similar Python code in a Jupyter notebook (see examples elsewhere).


The code in this module (=Python file) assumes that the Data file (the Excel file)
 contains data in the following columns:
 Custom_Item	Number_Of_Importers	Number_Of_Agents	Number_Of_Declarations	Confirmers	Regulations

If this data does not exist, there is nothing to plot.

Adding that data (COLUMN_NAME_NUMBER_OF_ISHURIM) to the data file is done by code in other modules! (doProcessing.py)

For plotting graphs to work correctly, the RESULTS_FILE/dataFrame should have the following columns:
 Custom_Item	Number_Of_Importers	Number_Of_Agents	Number_Of_Declarations	Confirmers	Regulations

This code is meant to run as a Python script on a desktop/laptop computer.
You can probably copy/paste it into a Jupyter notebook, it will work with few changes.

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


def count_ishurim(list_of_regulations):
    print(list_of_regulations)
    return 1


def add_count_ishurim(file_df):
    for ind in file_df.index:
        list_of_regulations_as_str = file_df.at[ind, 'Regulations']
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


def do_some_plotting():
    df = calculate_dataframe()
    #df[COLUMN_NAME_NUMBER_OF_ISHURIM].plot()
    #plt.plot(df.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM])
    # Create scatter plot:
    #print('number of items:', df.shape[0])

    #plot_scatter_number_of_ishurim_to_importers(df)
    #plot_scatter_number_of_ishurim_to_declarations(df)
    #plot_scatter_number_of_ishurim_to_agents(df)

    #plot_scatter_number_of_gormim_to_importers(df)
    #plot_pie_of_number_of_ishurim(df)
    #plot_bar_of_number_of_ishurim(df)
    plot_bar_of_number_of_gormim(df)

def plot_scatter_number_of_ishurim_to_importers(df):
    plt.scatter(df[COLUMN_NAME_NUMBER_OF_ISHURIM], df[COLUMN_NAME_NUMBER_OF_IMPORTERS]
                , color='green', marker='o', linestyle='dashed', linewidth=2)
    plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר יבואנים ביחס למספר אישורים נדרשים  "[::-1] )   # reverse string because it is in Hebrew
    plt.show()


def plot_scatter_number_of_ishurim_to_declarations(df):
    plt.scatter(df[COLUMN_NAME_NUMBER_OF_ISHURIM], df[COLUMN_NAME_NUMBER_OF_DECLARATIONS]
                , color='green', marker='o', linestyle='dashed', linewidth=2)
    plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר הצהרות ביחס למספר אישורים נדרשים  "[::-1] )   # reverse string because it is in Hebrew
    plt.show()


def plot_scatter_number_of_ishurim_to_agents(df):
    plt.scatter(df[COLUMN_NAME_NUMBER_OF_ISHURIM], df[COLUMN_NAME_NUMBER_OF_AGENTS]
                , color='green', marker='o', linestyle='dashed', linewidth=2)
    plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר סוכנים ביחס למספר אישורים נדרשים  "[::-1] )   # reverse string because it is in Hebrew
    plt.show()


def plot_scatter_number_of_gormim_to_importers(df):
    plt.scatter(df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM], df[COLUMN_NAME_NUMBER_OF_IMPORTERS]
                , color='green', marker='o', linestyle='dashed', linewidth=2)
    plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר יבואנים ביחס למספר גורמים מאשרים נדרשים  "[::-1] )   # reverse string because it is in Hebrew
    plt.show()


def plot_pie_of_number_of_ishurim(df):
    x = df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts()
    list1 = list(zip(x.index, x.values))
    plt.pie(df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts(), labels=x.index)
    plt.title("Number of Ishurim")
    plt.show()


def plot_bar_of_number_of_ishurim(df):
    x = df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts()
    x2 = df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM].value_counts()
    p1 = plt.bar(x.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts())
    #plt.barh(x.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts())
    ss =  "(םיטירפ " + str(df.shape[0]) + " כהס) "
    ss2 = "מספר הפריטים שעבורם נדרש מספר אישורים "
    title = ss+ss2[::-1]
    plt.title(title) #"Number of Ishurim")

    plt.ylabel('Number of items')
    plt.xlabel('Number of Required Regulations')
    #plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    #plt.yticks(np.arange(0, 81, 10))
    #plt.legend((p[0]), ('Men'))

    plt.show()


def plot_bar_of_number_of_gormim(df):
    x2 = df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM].value_counts()
    p1 = plt.bar(x2.index, df[COLUMN_NAME_NUMBER_OF_GORMIM_MEASHRIM].value_counts())
    # for a horizintal bar graph, use barh:
    # plt.barh(x.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM].value_counts())
    ss = "(םיטירפ " + str(df.shape[0]) + " כהס) "
    ss2 = "מספר הפריטים שעבורם נדרש מספר גורמים מאשרים "
    title = ss+ss2[::-1]
    plt.title(title)  # "Number of Ishurim")

    plt.ylabel('Number of items')
    plt.xlabel('מספר גורמים מאשרים'[::-1])
    plt.show()



def just_plot():
    #existingDF = read_existing_results_file()
    do_some_plotting()


def main():
    do_some_plotting()





if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
    #just_plot()
