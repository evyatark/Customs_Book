# Python code to read Excel file

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# imports for scraping
from urllib.request import urlopen
from bs4 import BeautifulSoup

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
# import urllib.request

import datetime

"""
Creating an Excel "work file" from a specified Excel source file.

Uses Pandas method to read and write Excel files.

1. The basic data is read from the Excel file named "./טבלה מרכזית.xlsx"

The "source file" is the Excel file named "./טבלה מרכזית.xlsx".

The "work file" is the Excel file named NAME_OF_RESULTS_FILE ("my_customs_items.xlsx") in the current directory.

usage:
from createExcelWorkFile import create_work_file
create_work_file()
"""

NAME_OF_SOURCE_FILE = "./טבלה מרכזית.xlsx"
NAME_OF_RESULTS_FILE = "my_customs_items2.xlsx"

# The following column names depend on the file "טבלה מרכזית.xlsx"
# if you supply another (newer) file with different column names, you must change here!
ORIGINAL_COLUMN_NAME_NUMBER_OF_IMPORTERS = "כמות היבואנים עם זיהוי"
ORIGINAL_COLUMN_NAME_NUMBER_OF_AGENTS = "כמות סוכנים"
ORIGINAL_COLUMN_NAME_NUMBER_OF_DECLARATIONS = "ספירת הצהרות"
ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_1 = "פרט מכס"
ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_2 = "פרט מכס"
ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_3 = "פרט"

# The following column names will be used by code in other python files in this project!
NEW_COLUMN_NAME_NUMBER_OF_IMPORTERS = "Number_Of_Importers"
NEW_COLUMN_NAME_NUMBER_OF_AGENTS = "Number_Of_Agents"
NEW_COLUMN_NAME_NUMBER_OF_DECLARATIONS = "Number_Of_Declarations"
NEW_COLUMN_NAME_CUSTOM_ITEM = "Custom_Item"


def read_excel_file(filename):
    """
    From the specified Excel file (it would normally be NAME_OF_SOURCE_FILE),
     read ONLY the data in second, third and forth tabs!
    Then join data of all 3 tabs to one DataFrame.
    The join is according to custom-item-full-classification.
    Note that each tab has a slightly DIFFERENT list of items!
    :param filename: name of the source file. Could be full path, otherwise it is assumed to be in current directory.
    :return: DataFrame with joined data
    """
    df1 = pd.read_excel(filename, sheet_name=1)
    df1 = df1.rename(columns={ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_1: NEW_COLUMN_NAME_CUSTOM_ITEM, ORIGINAL_COLUMN_NAME_NUMBER_OF_IMPORTERS:NEW_COLUMN_NAME_NUMBER_OF_IMPORTERS})
    df1 = df1.astype({NEW_COLUMN_NAME_CUSTOM_ITEM: str}, errors='raise')
    df1 = df1.set_index(NEW_COLUMN_NAME_CUSTOM_ITEM)

    df2 = pd.read_excel(filename, sheet_name=2)
    df2 = df2.rename(columns={ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_2: NEW_COLUMN_NAME_CUSTOM_ITEM, ORIGINAL_COLUMN_NAME_NUMBER_OF_AGENTS:NEW_COLUMN_NAME_NUMBER_OF_AGENTS})
    df2 = df2.astype({NEW_COLUMN_NAME_CUSTOM_ITEM: str}, errors='raise')
    df2 = df2.set_index(NEW_COLUMN_NAME_CUSTOM_ITEM)

    df3 = pd.read_excel(filename, sheet_name=3)
    df3 = df3.rename(columns={ORIGINAL_COLUMN_NAME_CUSTOM_ITEM_TAB_3: NEW_COLUMN_NAME_CUSTOM_ITEM, ORIGINAL_COLUMN_NAME_NUMBER_OF_DECLARATIONS:NEW_COLUMN_NAME_NUMBER_OF_DECLARATIONS})
    df3 = df3.astype({NEW_COLUMN_NAME_CUSTOM_ITEM: str}, errors='raise')
    df3 = df3.set_index(NEW_COLUMN_NAME_CUSTOM_ITEM)

    # Using outer join - This will work in any order of merges!!
    df = df1.copy()
    df = df.merge(df2, how="outer", left_on=NEW_COLUMN_NAME_CUSTOM_ITEM, right_on=NEW_COLUMN_NAME_CUSTOM_ITEM, indicator=False)
    df = df.merge(df3, how="outer", left_on=NEW_COLUMN_NAME_CUSTOM_ITEM, right_on=NEW_COLUMN_NAME_CUSTOM_ITEM, indicator=False)
    df = df.sort_index()
    print(df.tail(40))
    return df;


def read_existing_results_file():
    df = None
    try:
        df = pd.read_excel(NAME_OF_RESULTS_FILE, sheet_name=0, index_col=0)
    except FileNotFoundError:
        print('file', NAME_OF_RESULTS_FILE, 'not found!')
        return None
    # change type
    df.index = df.index.astype(str)
    return df


def write_to_excel_file(df):
    excel_file = pd.ExcelWriter(NAME_OF_RESULTS_FILE)
    df.to_excel(excel_writer=excel_file, sheet_name="items", index=True)
    excel_file.save()


def create_if_no_previous_results():
    df = read_excel_file(NAME_OF_SOURCE_FILE)
    print('not scraped:', df.shape[0])
    resulting_df = df
    write_to_excel_file(resulting_df)


def create_work_file():
    existing_df = read_existing_results_file()
    if existing_df is None:
        create_if_no_previous_results()
    else:
        print("work file already exists")


if __name__ == "__main__":
    # read_excel_file(NAME_OF_SOURCE_FILE)
    startedAt = datetime.datetime.now()
    create_work_file()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
