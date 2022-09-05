# Python code for web scraping of ShaarOlamy web-site

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



#NAME_OF_RESULTS_FILE = "my_customs_items.xlsx"
NUMBER_OF_ITEMS_TO_SCRAPE = 1000


def make_request(url, headers=None, data=None):
    request = Request(url, headers=headers or {}, data=data)
    try:
        with urlopen(request, timeout=10) as response:
            #print(response.status)
            return response.read(), response, response.status
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")


def retrieveCustomsItemId(fullClassification):
    """
    Do a Web Scraping session of ShaarOlamy web-site,
    retrieving the customsItemId from the given FullClassification (of a customsItem)
    (This requires a POST request to ShaarOlami)
    :param fullClassification: 10-digits "name" of customs-item
    :return:
    """
    #print('FullClassification=', fullClassification)
    url = 'https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/CustomsTaarifEntry'
    #post_dict = {"FullClassification": "2009129000"}
    post_dict = {"FullClassification": fullClassification}
    url_encoded_data = urlencode(post_dict)
    post_data = url_encoded_data.encode("utf-8")
    body, response, status = make_request(url, data=post_data)
    #print('status=', status)
    html = body.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    # The customItemID of the item (used in the URL, and also in SQL tables)
    items = soup.find_all("li")
    if len(items) <= 0:
        return ''   # no item found for this fullClassification
    last = items[-1]
    itemId = last.attrs["id"]
    #print('id=', itemId)
    return itemId


def removeUnPrintableCaracters(str):
    if str.isprintable():
        return str
    ret = ""
    for x in str:
        if (x.isprintable()):
            ret = ret + x
        else:
            ret = ret + '~'
    return ret


def findTd(tr, index):
    #return "'" + tr.find_all("td")[index].text.strip() + "'"
    return tr.find_all("td")[index].text.strip()


def findPageByUrl(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def parseDrishotTable(drishotTable):
    if not drishotTable:
        #print('no Drishot')
        return []
    drishotList = []
    drishotBody = drishotTable.find("tbody")
    trs = drishotBody.find_all("tr")
    for tr in trs:
        ishur = []
        for i in range(1, 11):
            ishur.append(findTd(tr, i))
        # print(findTd(tr, 1), findTd(tr, 2), findTd(tr, 3), findTd(tr, 4), findTd(tr, 5)
        #          #,findTd(tr, 6), findTd(tr, 7), findTd(tr, 8), findTd(tr, 9), findTd(tr, 10)
        #          )
        drishotList.append(ishur)
    return drishotList


def parseIshurim(ishurimList):
    """
    receive a list of Ishurim details, parse and return list of unique ids of Ishurim
    (such as: 'משרד הבריאות' 'אישור שירות המזון (0701) -'
    will be '0701')
    :param ishurimList:
    :return:
    """
    setOfIshurIds = set(())
    for ishur in ishurimList:
        goremMeasher = ishur[3]
        sugIshur = ishur[4]
        if sugIshur:
            ishurId = parseSugIshur(sugIshur)
            if ishurId != '':
                setOfIshurIds.add(ishurId)
        #print(setOfIshurIds)
    return list(setOfIshurIds)


def parseSugIshur(ishurStr):
    """
    usually ishurStr will be like:
    'רשיון הרשות לתכנון חקלאות וכלכלה (0110)'
    and we want to extract '0110'
    :param ishurStr:
    :return:
    """
    value = 'QQQ'

    if ishurStr == 'אישור הוועדה לאנרגיה אטומית':
        return ishurStr # no numeric code for this Ishur!

    #print('==>', ishurStr)
    splitted = ishurStr.split()
    #print('1==>', splitted[-1])
    #print('2==>', splitted[-2])
    #print('3==>', splitted[-3])
    last = splitted[-1]
    if last == '-':
        last = splitted[-2]
    elif last == ')':    # case of  משרד החקלאות אישור המנכ"ל (0107)
        last = splitted[-2]
    #print(last)
    if last.startswith('(') and last.endswith('))'):    # case of 2303
        value = last[1:-2]
    else:
        if last.startswith('(') and last.endswith(')'):
            value = last[1:-1]
            #return value
        else:
            # case of 0702
            last = splitted[3]  # a ['אישור', 'אגף', 'הרוקחות', '(0702)', '(', 'אישור', 'אגף', 'הרוקחות', '(0702)', '-', ',', 'אישור', 'אגף', 'הרוקחות', '(0702)', '-', 'דם', 'ורקמות', ')']
        if last.startswith('(') and last.endswith(')'):
            value = last[1:-1]
            # return value
        else:
            # case of 0303
            last = splitted[2]        # a ['אישור', 'מנכ"ל', '(0303)', '(', 'אישור', 'מנכ"ל', '(0303)', '-', ',', 'אישור', 'מנכ"ל', '(0303)', '-', '0303', ')']
        if last.startswith('(') and last.endswith(')'):
            value = last[1:-1]

    if (value.isnumeric()):
        return value
    print("==> could not parse:", ishurStr)
    return ''

# ===> 2841610000 Unique Ishurim: Not Equal
# db: ['0308', '0311', '2303'] web: ['0308', '0311']
# ====> incorrect item full classification: 2844440000 2844400000
# ==> could not parse: אישור הוועדה לאנרגיה אטומית
# ===> 2844500000 Unique Ishurim: Not Equal
# db: ['0603', 'אישור אגף ניהול משאבי תשתיות'] web: ['0603']


def scrapeAll(customsItemId):
    url = "https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/ImportCustomsItemDetails?customsItemId=" + str(customsItemId)
    soup = findPageByUrl(url)

    # most detailed customItem ('2009111910/5': 10 digits + slash + additional digit)
    items = soup.find_all("span", class_="treeTitle")
    #print(customsItemId, ' ##')
    #print('=================================')
    if (len(items) == 0):
        print('for item id', customsItemId, 'add validDate')
        soup = findPageByUrl(url + '&validToDate=12%2F31%2F2021%2000%3A00%3A00')
        items = soup.find_all("span", class_="treeTitle")
    if (len(items) == 0):
        #        print(customsItemId, ' ##')
        return
    item = soup.find_all("span", class_="treeTitle")[-1]
    customItem = item.text.strip()

    drishotTable = soup.find("table", class_="legalDemandsTable")
    if drishotTable:
        drishotBody = drishotTable.find("tbody")
        trs = drishotBody.find_all("tr")
        #print(len(trs))
        # for tr in trs:
        #     print(findTd(tr, 1), findTd(tr, 2), findTd(tr, 3), findTd(tr, 4), findTd(tr, 5)
        #          #,findTd(tr, 6), findTd(tr, 7), findTd(tr, 8), findTd(tr, 9), findTd(tr, 10)
        #          )
    else:
        print('no Drishot')

    ishurim = parseDrishotTable(drishotTable)
    #print('number of Ishurim=', len(ishurim))
    ishurIdList = parseIshurim(ishurim)
    #print(ishurIdList)
    #print('number of unique Ishurim=', len(ishurIdList))
    return (customItem, customsItemId, ishurIdList, ishurim)


def extractCustomItemsAsListFromExistingFile(df):
    """
    if a results file already exists, some of its lines will contain an extraction date
    (for each item that was already extracted)
    We will use that information to not scrape items that were already scraped less than X days ago.

    :param df:
    :return:
    """
    # the column named 'extracted_at_date' contains date when this item was extracted
    condition = df["extracted_at_date"].isnull()
    df1 = df[condition]
    # print(df.head(5))
    # print(df1.head(5))
    return df1.index.values.tolist()


def extractCustomItemsAsList(df):
    return df.index.values.tolist()


def do_merge(df1, df2):
    df = df1.merge(df2, how="outer", left_on="Custom_Item", right_on="Custom_Item", indicator=False)
    return df


def addNumberOfIshurimToDataFrame(df, listOfAllResults):
    print(listOfAllResults)
    df4 = pd.DataFrame(listOfAllResults, columns = ['Custom_Item', 'itemId', 'numberOfIshurim', 'full_classification_with_additional_digit', 'extracted_at_date'])
    df4 = df4.set_index("Custom_Item")
    print(df4)
    df = do_merge(df, df4)
    df = df.sort_index()
    # print(df.head(10))
    return df


def checkCorrectness(fullClassWithAdditionalDigit, fullClassification):
    withoutLastDigit = fullClassWithAdditionalDigit
    if '/' in withoutLastDigit:
        index = withoutLastDigit.rfind('/')
        withoutLastDigit = withoutLastDigit[:index]
    if withoutLastDigit != fullClassification:
        print('====> incorrect item full classification:', withoutLastDigit, fullClassification)


def divideExistingResultsDF(existingDF):
    condition_scraped_lines = existingDF["extracted_at_date"].notnull()     # TODO expand this condition to include items that wre scraped more than X days ago
    scraped_df = existingDF[condition_scraped_lines]
    condition_non_scraped_lines = existingDF["extracted_at_date"].isnull()  # TODO same as above
    not_scraped_df_all = existingDF[condition_non_scraped_lines]
    # in not_scraped_df, remove the additional columns ("Custom_Item" is index)
    not_scraped_df = not_scraped_df_all[[ "כמות היבואנים עם זיהוי", "כמות סוכנים", "ספירת הצהרות"]]
    return scraped_df, not_scraped_df


def addToPreviousResults(existingDF):
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


def scrapeOneItem(fullClassification):
    """
    perform a Web Scraping of a single customs-item
    :param fullClassification:
    :return: a list of data, or None (if some exception happened during scraping)
    """
    fullClassificationStr = str(fullClassification)
    itemId = retrieveCustomsItemId(fullClassification)
    item = None
    numberOfUniqueIshurim = None
    ishurim = None
    fullClassWithAdditionalDigit = None
    listOfUniqueIshurim = []
    if itemId == '':
        print('====>', fullClassification, 'no data found!')
        # no data found in CustomsBook web site for this item!
        # but we do add a scraping date in the results df (so subsequent processing will know not to process this item again!)
    else:
        try:
            fullClassWithAdditionalDigit, item, listOfUniqueIshurim, ishurim = scrapeAll(itemId)
            numberOfUniqueIshurim = len(listOfUniqueIshurim)
            checkCorrectness(fullClassWithAdditionalDigit,
                             fullClassificationStr)  # we already have the fullClassification without the additional digit. checking to be sure...
        except:
            print('====> unknown error for item', fullClassificationStr)
            return (None, None)
    currentDate = str(datetime.datetime.now()).split(' ')[0]
    list1 = [fullClassificationStr, item, numberOfUniqueIshurim, fullClassWithAdditionalDigit, currentDate, listOfUniqueIshurim]
    return (list1, ishurim)


def scrapeAccordingToList(customsItemFullClassificationList, howManyItemsToScrape):
    listOfAllResults = []
    detailedResults = dict()
    for fullClassification in customsItemFullClassificationList[0:howManyItemsToScrape]:
        list1, listOfIshurim = scrapeOneItem(fullClassification)
        # first part of result is list of: [Full Classification, item ID, Number of Ishurim, Full Classification including additional digit, date of scraping, listOfUniqueIshurim]
        # ['4706100000', '14842', 2, '4706100000/7', '2022-08-23', ['0308', '0311']]
        # second part - listOfIshurim is:
        x=\
        [
            ['תוספת 1 לצו יבוא חופשי', '\u200e4706000000', 'שנשמרו או חוסנו בחומרים המכילים זרניך )ארסן( אנאורגני או כרום שש ערכי או שניהם,', 'משרד הכלכלה', 'רישיון מינהל סביבה ופיתוח בר קיימא (0311)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה'],
            ['תוספת 1 לצו יבוא אישי', '\u200e4706000000', 'שנשמרו או חוסנו בחומרים המכילים זרניך )ארסן( אנאורגני או כרום שש ערכי או שניהם', 'משרד הכלכלה', 'רישיון מינהל תעשיות (0308)', '', 'כל התנאים', 'כן', 'לא', 'ישראל ואוטונומיה']
        ]

        if list1 is not None:
            listOfAllResults.append(list1)
            detailedResults[fullClassification] = listOfIshurim
    return listOfAllResults, detailedResults


def processItemsNeverScrapedBefore(df):
    # the df contains columns as if read from original file ("./טבלה מרכזית.xlsx")
    customsItemFullClassificationList = extractCustomItemsAsList(df)
    #   NUMBER_OF_ITEMS_TO_SCRAPE = 3
    howManyItemsToScrape = NUMBER_OF_ITEMS_TO_SCRAPE
    if len(customsItemFullClassificationList) < NUMBER_OF_ITEMS_TO_SCRAPE:
        howManyItemsToScrape = customsItemFullClassificationList
    if howManyItemsToScrape <= 0:
        print('=====> No items to scrape!', 'All of', NUMBER_OF_ITEMS_TO_SCRAPE,
              'were already scraped...')  # TODO at date...
        exit(-1)
    scrapingResults = scrapeAccordingToList(customsItemFullClassificationList, howManyItemsToScrape)
    resulting_df = addNumberOfIshurimToDataFrame(df, scrapingResults)
    return resulting_df


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    # ['1101002000', '1206002000']
    # ['4706100000', '4706200000', '4706300000'], 3
    scrapingResults1 = scrapeAccordingToList(['1101002000', '1206002000'], 2)
    print(scrapingResults1)
    #processItemsNeverScrapedBefore(df_not_scraped)
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
    #just_plot()
