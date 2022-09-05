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
#import urllib.request

import datetime

"""
To create plots of various calculations, use Pandas and Matplotlib on the Excel file.

Using Pandas/Matplotlib can be done either executing code in this Python file,
or by executing similar Python code in a Jupyter notebook (see examples elsewhere).

The Excel file named NAME_OF_RESULTS_FILE ("my_customs_items.xlsx") in the current directory
is the Data file that should be used for all data processing that are meant to produce results
(either as tables, or as plots).

The Excel file ("my_customs_items.xlsx") does NOT contain data of all customs-items!
This data must first be collected and written to the Excel file.
This is currently done by Python code in this file (but will be separated to separate Python files)!

Data in The Excel file can be collected from the following sources:
1. The basic data is read from the Excel file named "./טבלה מרכזית.xlsx"
(this will be separated to Python file XXX.py)
2. For each customs-item, the Python code navigates to the web-site of Shaar-Olamy
   and does some Web-Scraping to fetch and process data regarding that specific customs-item
(this will be separated to Python file XXX.py)
3. As an alternative to #2, we can write Python code that the MySQL database exported from Shaar-Olamy.
(this will be separated to Python file XXX.py)

"""

from readWriteExcelFile import create_work_file, read_existing_results_file, write_to_excel_file
from scrapeShaarOlamy import processItemsNeverScrapedBefore, scrapeAccordingToList, scrapeOneItem, \
    extractCustomItemsAsList
from readDB import retrieve_for_all_parents, connect




def divideExistingResultsDF(existingDF):
    condition_scraped_lines = existingDF["extracted_at_date"].notnull()     # TODO expand this condition to include items that wre scraped more than X days ago
    scraped_df = existingDF[condition_scraped_lines]
    condition_non_scraped_lines = existingDF["extracted_at_date"].isnull()  # TODO same as above
    not_scraped_df_all = existingDF[condition_non_scraped_lines]
    # in not_scraped_df, remove the additional columns ("Custom_Item" is index)
    not_scraped_df = not_scraped_df_all[[ "כמות היבואנים עם זיהוי", "כמות סוכנים", "ספירת הצהרות"]]
    return scraped_df, not_scraped_df


# addToPreviousResults
def processMoreItemsAndAddToPreviousResults(existingDF):
    # existingDF already contains the content of the existing file
    # we divide it to 2 dataFrames - one with the lines that already have scraping results,
    # the other - with lines that were not processed
    df_scraped, df_not_scraped = divideExistingResultsDF(existingDF)
    print('already scraped:', df_scraped.shape[0])
    print('not scraped:', df_not_scraped.shape[0])
    print("==> scraping...")
    results_of_new_scraped_df = processItemsNeverScrapedBefore(df_not_scraped)
    # now concat df_scraped and results_of_new_scraped_df, they should have exactly the same columns!
    concatenated_df = pd.concat(objs=[df_scraped, results_of_new_scraped_df])
    #writeToExcelFile(concatenated_df)   # this overwrites the previous file??
    return concatenated_df




def detailedCompare(scrapingResults1, detailedScrapingResults, list_of_regulations_from_DB):
    """
    === Comparing Results ====================================
------- from scraping: -------------------
number of Ishurim= 14
['0701', '0705', '0102', '0101']
number of unique Ishurim= 4
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'אחריםלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'אחריםלא כולל 1006300000,', 'משרד הבריאות', 'אישור שחרור תחנת מעבר (0705) -', '', 'כל התנאים', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'למאכל אדם ארוזים למכירה בקמעונאותלא כולל 1006300000,', 'משרד הבריאות', 'אישור שחרור תחנת מעבר (0705) -', '', 'כל התנאים', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'להזנת בעלי חייםלא כולל 1006300000,', 'משרד הבריאות', 'אישור שחרור תחנת מעבר (0705) -', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'אחריםלא כולל 1006300000,', 'משרד הבריאות', 'אישור שירות המזון (0701) -', '', 'כל התנאים', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'למאכל אדם ארוזים למכירה בקמעונאותלא כולל 1006300000,', 'משרד הבריאות', 'אישור שירות המזון (0701) -', '', 'כל התנאים', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'לזריעהלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'להזנת בעלי חייםלא כולל 1006300000,', 'משרד הבריאות', 'אישור שירות המזון (0701) -', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'להזנת בעלי חייםלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא חופשי', '\u200e1000000000', 'למעט 10.06.3000לא כולל 1006300000,', '', '', '', 'כותרת', 'לא', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא אישי', '\u200e1000000000', 'להזנת בעלי חייםלא כולל 1006300000,', 'משרד החקלאות', 'אישור השירות הוטרינרי (0101)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא אישי', '\u200e1000000000', 'אחריםלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא אישי', '\u200e1000000000', 'לזריעהלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
['תוספת 2 לצו יבוא אישי', '\u200e1000000000', 'להזנת בעלי חייםלא כולל 1006300000,', 'משרד החקלאות', 'אישור הגנת הצומח (0102)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
---------- from DB: ----------------
[('21556', '1003100000'), ('9804', '1003000000'), ('2157', '1000000000'), ('11984', 'II')]
{'order': 18, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '8104', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 19, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '8105', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 20, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5873', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '8106', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 21, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5874', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'למאכל אדם ארוזים למכירה בקמעונאות', 'RegularityRequiredCertificateID': '8107', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 22, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '8109', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 30, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8320', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '10757', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 31, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8322', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '10758', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 32, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8324', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'אחרים', 'RegularityRequiredCertificateID': '10759', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 44, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8320', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '12066', 'ConfirmationTypeID': '1-0101', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
{'order': 45, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '13149', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 46, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5874', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'למאכל אדם ארוזים למכירה בקמעונאות', 'RegularityRequiredCertificateID': '13150', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 47, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '13151', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'}
{'order': 48, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '13152', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}
--------------------------

    :param scrapingResults1:
    :param detailedScrapingResults:
    :param list_of_regulations_from_DB:
    :return:
    """
    fullCl = scrapingResults1[0]
    scrape_numberOfUniqueIshurim = scrapingResults1[2]
    scrape_listOfUniqueIshurim = sorted( scrapingResults1[5] )
    db_allIshurim = [item["ConfirmationTypeID"] for item in list_of_regulations_from_DB]
    db_listOfIshurim = [item.split("-")[1] for item in db_allIshurim]
    db_listOfUniqueIshurim = sorted( list(set(db_listOfIshurim)) )
    db_numberOfUniqueIshurim = len(db_listOfUniqueIshurim)
    #print(fullCl)
    #print("db:", db_numberOfUniqueIshurim, "web:", scrape_numberOfUniqueIshurim)
    if db_listOfUniqueIshurim == scrape_listOfUniqueIshurim:
        #print("Unique Ishurim: Equal")
        return True
    else:
        print("===>", fullCl, "Unique Ishurim: Not Equal")
        print("db:", db_listOfUniqueIshurim, "web:", scrape_listOfUniqueIshurim)
        return False


def compareResults(scrapingResults1, detailedScrapingResults, list_of_regulations_from_DB):
    #print('=== Comparing Results for', scrapingResults1[0], '====================================')
    result = detailedCompare(scrapingResults1, detailedScrapingResults, list_of_regulations_from_DB)
    if (False):
        print('------- from scraping: -------------------')
        for result in detailedScrapingResults:
            print(result)
        print('---------- from DB: ----------------')
        for row in list_of_regulations_from_DB:
            print(row)
        print('--------------------------')


def runBothAndCompareResults(fullClassification):
    # fullClassification can be '4706100000'
    try:
        scrapingResults1, detailedScrapingResults = scrapeOneItem(fullClassification)
        if scrapingResults1 is None:
            print("scraping failed")
            return
        itemId = scrapingResults1[1]
        if itemId is None:
            print("scraping could not find item ID")
            return
        list_of_regulations_from_DB = retrieve_for_all_parents(connect(), itemId)
        compareResults(scrapingResults1, detailedScrapingResults, list_of_regulations_from_DB)
    except:
        print("some unknown exception for FullClassification", fullClassification)

def test():
    # ['1101002000', '1206002000']
    # ['4706100000', '4706200000', '4706300000']
    runBothAndCompareResults('1509903200')

# we have a problem with this fullClassification:
# ===> 2844500000 Unique Ishurim: Not Equal
# db: ['0603', 'אישור אגף ניהול משאבי תשתיות'] web: ['0603', 'אישור הוועדה לאנרגיה אטומית']
# some unknown exception for FullClassification 1509903200
# some unknown exception for FullClassification 1905403000


def test2():
    known_issues = ['1509903200']
    start = 0
    end = 1000
    print("comparing", str(end-start), "items...")
    df = read_existing_results_file()
    customsItemFullClassificationList = extractCustomItemsAsList(df)    # 7113 items in this list!!
    # print("I have a list of items:", len(customsItemFullClassificationList))
    for fullClassification in customsItemFullClassificationList[start:end]:
        if fullClassification in known_issues:
            continue
        runBothAndCompareResults(fullClassification)


def main():
    create_work_file()
    existingDF = read_existing_results_file()
    newDF = processMoreItemsAndAddToPreviousResults(existingDF)
    write_to_excel_file(newDF)


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    # main()
    test2()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
    # just_plot()


"""
/home/evyatar/.pyenv/versions/pandas3/bin/python /home/evyatar/work/python/pandas3/doProcessing.py 
comparing 1000 items...
====> 101210000 no data found!
scraping could not find item ID
====> 101290000 no data found!
scraping could not find item ID
====> 102293000 no data found!
scraping could not find item ID
====> 103100000 no data found!
scraping could not find item ID
====> 103911000 no data found!
scraping could not find item ID
====> 103919000 no data found!
scraping could not find item ID
====> 104101000 no data found!
scraping could not find item ID
====> 104109000 no data found!
scraping could not find item ID
====> 105110000 no data found!
scraping could not find item ID
====> 105129000 no data found!
scraping could not find item ID
====> 105139000 no data found!
scraping could not find item ID
====> 106110000 no data found!
scraping could not find item ID
====> 106140000 no data found!
scraping could not find item ID
====> 106190000 no data found!
scraping could not find item ID
====> 106200000 no data found!
scraping could not find item ID
====> 106310000 no data found!
scraping could not find item ID
====> 106391900 no data found!
scraping could not find item ID
====> 106399000 no data found!
scraping could not find item ID
====> 106410000 no data found!
scraping could not find item ID
====> 106490000 no data found!
scraping could not find item ID
====> 106900000 no data found!
scraping could not find item ID
for item id 5294 add validDate
for item id 29856 add validDate
for item id 14561 add validDate
for item id 14872 add validDate
for item id 4984 add validDate
====> 1905909100 no data found!
scraping could not find item ID
for item id 571 add validDate
for item id 30202 add validDate
====> unknown error for item 2002109000
scraping failed
for item id 30203 add validDate
====> unknown error for item 2002901400
scraping failed
for item id 29871 add validDate
===> 2008999000 Unique Ishurim: Not Equal
db: [] web: ['0701', '0705']
====> incorrect item full classification: 2009111190 2009111100
====> incorrect item full classification: 2009111990 2009111900
====> incorrect item full classification: 2009112900 2009112000
====> incorrect item full classification: 2009191190 2009191100
====> incorrect item full classification: 2009191990 2009191900
====> incorrect item full classification: 2009199900 2009199000
====> incorrect item full classification: 2009291190 2009291100
====> incorrect item full classification: 2009291390 2009291300
====> incorrect item full classification: 2009299900 2009299000
====> incorrect item full classification: 2009311900 2009311000
====> incorrect item full classification: 2009319900 2009319000
====> incorrect item full classification: 2009391190 2009391100
====> incorrect item full classification: 2009391990 2009391900
====> incorrect item full classification: 2009399900 2009399000
====> incorrect item full classification: 2009499000 2009490000
for item id 29971 add validDate
for item id 30000 add validDate
for item id 29972 add validDate
====> incorrect item full classification: 2009793190 2009793100
====> incorrect item full classification: 2009793990 2009793900
====> incorrect item full classification: 2009799900 2009799000
====> incorrect item full classification: 2009811190 2009811100
====> incorrect item full classification: 2009811990 2009811900
====> incorrect item full classification: 2009891190 2009891100
====> incorrect item full classification: 2009891290 2009891200
====> incorrect item full classification: 2009891390 2009891300
====> incorrect item full classification: 2009891490 2009891400
====> incorrect item full classification: 2009891590 2009891500
====> incorrect item full classification: 2009891690 2009891600
====> incorrect item full classification: 2009891790 2009891700
====> incorrect item full classification: 2009891890 2009891800
====> incorrect item full classification: 2009891990 2009891900
====> incorrect item full classification: 2009893900 2009893000
====> incorrect item full classification: 2009899900 2009899000
====> incorrect item full classification: 2009901190 2009901100
====> 201200000 no data found!
scraping could not find item ID
====> 201300000 no data found!
scraping could not find item ID
====> 202200000 no data found!
scraping could not find item ID
====> 202300000 no data found!
scraping could not find item ID
====> 203290000 no data found!
scraping could not find item ID
====> 204220000 no data found!
scraping could not find item ID
====> 204420000 no data found!
scraping could not find item ID
====> 204430000 no data found!
scraping could not find item ID
====> 206210000 no data found!
scraping could not find item ID
====> 206220000 no data found!
scraping could not find item ID
====> 206290000 no data found!
scraping could not find item ID
====> 206900000 no data found!
scraping could not find item ID
====> 207140000 no data found!
scraping could not find item ID
====> 207420000 no data found!
scraping could not find item ID
====> 207459000 no data found!
scraping could not find item ID
====> 207551000 no data found!
scraping could not find item ID
====> 207559000 no data found!
scraping could not find item ID
====> 209900000 no data found!
scraping could not find item ID
====> incorrect item full classification: 2106905900 2106905000
====> incorrect item full classification: 2106909599 2106909500
====> incorrect item full classification: 2106909699 2106909600
====> incorrect item full classification: 2106909899 2106909800
====> incorrect item full classification: 2106909990 2106909900
====> 210991000 no data found!
scraping could not find item ID
====> incorrect item full classification: 2202109000 2202100000
====> incorrect item full classification: 2202919000 2202910000
====> incorrect item full classification: 2202999900 2202999000
for item id 19839 add validDate
for item id 29796 add validDate
for item id 29802 add validDate
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
for item id 12061 add validDate
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
====> incorrect item full classification: 2707209000 2707200000
====> incorrect item full classification: 2707309000 2707300000
====> incorrect item full classification: 2707509000 2707500000
====> incorrect item full classification: 2707999000 2707990000
no Drishot
no Drishot
no Drishot
====> incorrect item full classification: 2710122900 2710122000
====> incorrect item full classification: 2710194900 2710194000
====> incorrect item full classification: 2710199900 2710199000
====> incorrect item full classification: 2710202900 2710202000
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot
no Drishot

"""