# Python code to read Excel file
#
# This file is obsolete!!
#
# instead, use doProcessing.py
#


import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import datetime

from readWriteExcelFile import read_existing_results_file


"""
To create plots of various calculations, use Pandas and Matplotlib on the Excel file.

Using Pandas/Matplotlib can be done either executing code in this Python file,
or by executing similar Python code in a Jupyter notebook (see examples elsewhere).

The Excel file named NAME_OF_RESULTS_FILE ("my_customs_items.xlsx") in the current directory
is the Data file that should be used for all data processing that are meant to produce results
(either as tables, or as plots).

The code in this module (=Python file) assumes that the Data file contains data in columns such as COLUMN_NAME_NUMBER_OF_ISHURIM.
If this data does not exist, there is nothing to plot.

Adding that data (COLUMN_NAME_NUMBER_OF_ISHURIM) to the data file is done by code in other modules!
(specifically by addNumberOfIshurimToDataFrame() in scrapeShaarOlamy.py)

For plotting graphs to work correctly, the RESULTS_FILE/dataFrame should have the following columns:

Custom_Item     Number_Of_Importers ...     Number_Of_Ishurim

"""

# NAME_OF_RESULTS_FILE = "my_customs_items.xlsx"
# NUMBER_OF_ITEMS_TO_SCRAPE = 1000

COLUMN_NAME_NUMBER_OF_ISHURIM = "Number_Of_Ishurim"
COLUMN_NAME_NUMBER_OF_IMPORTERS = "Number_Of_Importers"


def check_if_df_contains_data_to_plot(df):
    if COLUMN_NAME_NUMBER_OF_ISHURIM in df:
        return True
    return False


def do_some_plotting():
    file_df = read_existing_results_file()
    if not check_if_df_contains_data_to_plot(file_df):
        print("===> Error: File does not contain required data")
        return
    condition_scraped_lines = file_df[COLUMN_NAME_NUMBER_OF_ISHURIM].notnull() # & file_df["כמות היבואנים עם זיהוי"].notnull()
    df = file_df[condition_scraped_lines]
    #df[COLUMN_NAME_NUMBER_OF_ISHURIM].plot()
    #plt.plot(df.index, df[COLUMN_NAME_NUMBER_OF_ISHURIM])
    # Create scatter plot:
    print('number of items:', df.shape[0])
    plt.scatter(df[COLUMN_NAME_NUMBER_OF_ISHURIM], df["כמות היבואנים עם זיהוי"]
                , color='green', marker='o', linestyle='dashed',
                linewidth=2
                )
    #plt.scatter(df["כמות היבואנים עם זיהוי"], df["numberOfIshurim"])
    plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר יבואנים ביחס למספר אישורים נדרשים  "[::-1] )   # reverse string because it is in Hebrew
    #plt.title( "(םיטירפ " + str(df.shape[0]) + ") " +  "מספר אישורים נדרשים ביחס למספר יבואנים"[::-1] )   # reverse string because it is in Hebrew
    plt.show()


def just_plot():
    existingDF = read_existing_results_file()
    do_some_plotting()


def main():
    do_some_plotting()





if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
    #just_plot()
