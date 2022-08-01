# Python code to read Excel file

import pandas as pd
import numpy as np

# imports for scraping
from urllib.request import urlopen
from bs4 import BeautifulSoup

from urllib.parse import urlencode
from urllib.request import urlopen, Request

import datetime


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


''' retrieving the customsItemId from the FullClassification of customsItem
(This requires a POST request to ShaarOlami)
'''
def retrieveCustomsItemId(fullClassification):
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
        print('no Drishot')
        return []
    drishotList = []
    drishotBody = drishotTable.find("tbody")
    trs = drishotBody.find_all("tr")
    for tr in trs:
        ishur = []
        for i in range(1, 11):
            ishur.append(findTd(tr, i))
        print(findTd(tr, 1), findTd(tr, 2), findTd(tr, 3), findTd(tr, 4), findTd(tr, 5)
                 #,findTd(tr, 6), findTd(tr, 7), findTd(tr, 8), findTd(tr, 9), findTd(tr, 10)
                 )
        drishotList.append(ishur)
    return drishotList


'''
receive a list of Ishurim details, parse and return list of unique ids of Ishurim
(such as: 
'משרד הבריאות' 'אישור שירות המזון (0701) -'
will be '0701'
)
'''
def parseIshurim(ishurimList):
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


'''
usually ishurStr will be like:
'רשיון הרשות לתכנון חקלאות וכלכלה (0110)'
and we want to extract '0110'
'''
def parseSugIshur(ishurStr):
    value = 'QQQ'
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
    if last.startswith('(') and last.endswith(')'):
        value = last[1:-1]
        #return value
    if (value.isnumeric()):
        return value
    return ''


def scrapeAll(customsItemId):
    url = "https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/ImportCustomsItemDetails?customsItemId=" + str(customsItemId)
    soup = findPageByUrl(url)

    # most detailed customItem ('2009111910/5': 10 digits + slash + additional digit)
    items = soup.find_all("span", class_="treeTitle")
    #print(customsItemId, ' ##')
    print('=================================')
    if (len(items) == 0):
        print('add validDate')
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
    print('number of Ishurim=', len(ishurim))
    ishurIdList = parseIshurim(ishurim)
    print(ishurIdList)
    print('number of unique Ishurim=', len(ishurIdList))
    return (customItem, customsItemId, len(ishurIdList))


def readExcelFile(filename):
    df1 = pd.read_excel(filename, sheet_name=1)
    df1 = df1.rename(columns={"פרט מכס":"Custom_Item"})
    df1 = df1.astype({"Custom_Item":str}, errors='raise')
    df1 = df1.set_index("Custom_Item")

    df2 = pd.read_excel(filename, sheet_name=2)
    df2 = df2.rename(columns={"פרט מכס":"Custom_Item"})
    df2 = df2.astype({"Custom_Item":str}, errors='raise')
    df2 = df2.set_index("Custom_Item")

    df3 = pd.read_excel(filename, sheet_name=3)
    df3 = df3.rename(columns={"פרט":"Custom_Item"})
    df3 = df3.astype({"Custom_Item":str}, errors='raise')
    df3 = df3.set_index("Custom_Item")

    # Using outer join - This will work in any orderof merges!!
    df = df1.copy()
    df = df.merge(df2, how="outer", left_on="Custom_Item", right_on="Custom_Item", indicator=False)
    df = df.merge(df3, how="outer", left_on="Custom_Item", right_on="Custom_Item", indicator=False)
    df = df.sort_index()
    #print(df.tail(40))
    return df;


def writeToExcelFile(df):
    excel_file = pd.ExcelWriter("my_customs_items.xlsx")
    df.to_excel(
        excel_writer=excel_file, sheet_name="items", index=True
    )
    excel_file.save()


def extractCustomItemsAsList(df):
    return df.index.values.tolist()


def addNumberOfIshurimToDataFrame(df, listOfAllResults):
    print(listOfAllResults)
    df4 = pd.DataFrame(listOfAllResults, columns = ['Custom_Item', 'itemId', 'numberOfIshurim', 'full_classification_with_additional_digit', 'extracted_at_date'])
    df4 = df4.set_index("Custom_Item")
    print(df4)

    df = df.merge(df4, how="outer", left_on="Custom_Item", right_on="Custom_Item", indicator=False)
    df = df.sort_index()
    print(df.head(10))
    return df


def checkCorrectness(fullClassWithAdditionalDigit, fullClassification):
    withoutLastDigit = fullClassWithAdditionalDigit
    if '/' in withoutLastDigit:
        index = withoutLastDigit.rfind('/')
        withoutLastDigit = withoutLastDigit[:index]
    if withoutLastDigit != fullClassification:
        print('====> incorrect item full classification:', withoutLastDigit, fullClassification)


def main():
    NUMBER_OF_ITEMS_TO_SCRAPE = 3
    df = readExcelFile("./טבלה מרכזית.xlsx")
    # print(df.tail(4))
    customsItemFullClassificationList = extractCustomItemsAsList(df)
    # print(customsItemFullClassificationList[1:10])

    # list = [3460, 27189]

    # for id in list:
    #     scrapeAll(id)
    #     retrieveCustomsItemId("2009129000")

    listOfAllResults = []
    for fullClassification in customsItemFullClassificationList[0:NUMBER_OF_ITEMS_TO_SCRAPE]:
        itemId = retrieveCustomsItemId(fullClassification)
        if itemId == '':
            print('====>', fullClassification, 'no data found!')
            continue    # no data found in CustomsBook web site for this item!
        fullClassWithAdditionalDigit, item, uniqueIshurim = scrapeAll(itemId)
        checkCorrectness(fullClassWithAdditionalDigit, fullClassification) # we already have the fullClassification without the additional digit. checking to be sure...
        currentDate = str(datetime.datetime.now()).split(' ')[0]
        list1 = [fullClassification, item, uniqueIshurim, fullClassWithAdditionalDigit, currentDate]
        listOfAllResults.append(list1)

    # print(listOfAllResults)
    # df4 = pd.DataFrame(listOfAllResults, columns = ['Custom_Item', 'itemId', 'numberOfIshurim'])
    # df4 = df4.set_index("Custom_Item")
    # print(df4)
    resulting_df = addNumberOfIshurimToDataFrame(df, listOfAllResults)
    writeToExcelFile(resulting_df)


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
