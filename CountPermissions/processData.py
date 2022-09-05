"""
ProcessData.py

functions in this module create data in the dataframe of the Excel file NAME_OF_RESULTS_FILE.

specifically, these functions use the DB processing from module readDB
to add (for each custom-item) data in the column COLUMN_NAME_NUMBER_OF_ISHURIM
(for a scatter plots:
 number-of-ishurim by number-of-importers
 number-of-ishurim by number-of-agents
 number-of-ishurim by number-of-declarations)

This function (main()) then adds 2 columns to the Excel file of the results: 'Confirmers' and 'Regulations' -
value in Confirmers will be like ['7', '3'] : "רשימת גורמים מאשרים"
value in Regulations will be like ['0308', '0701', '0702', '0705'] - list of codes of the required Ishurim for that item

an existing results file is expected to have the following columns:
COLUMN_NAME_CUSTOM_ITEM
COLUMN_NAME_NUMBER_OF_IMPORTERS
COLUMN_NAME_NUMBER_OF_AGENTS
COLUMN_NAME_NUMBER_OF_DECLARATIONS
COLUMN_NAME_EXTRACTED_AT_DATE

"""
from functools import reduce
import datetime

import readDB
import readWriteExcelFile
from readWriteExcelFile import read_existing_results_file, write_to_excel_file
from readDB import initialize_connection_and_caches, get_item_id_of_full_classification

COLUMN_NAME_CUSTOM_ITEM = readWriteExcelFile.NEW_COLUMN_NAME_CUSTOM_ITEM
COLUMN_NAME_NUMBER_OF_IMPORTERS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_IMPORTERS
COLUMN_NAME_NUMBER_OF_AGENTS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_AGENTS
COLUMN_NAME_NUMBER_OF_DECLARATIONS = readWriteExcelFile.NEW_COLUMN_NAME_NUMBER_OF_DECLARATIONS
COLUMN_NAME_EXTRACTED_AT_DATE = "extracted_at_date"


def add_column(df, column_name):
    pass


def divideExistingResultsDF(existingDF):
    """
    return a dataFrame with only the non-processed rows!!
    :param existingDF:
    :return:
    The existing dataFrame is expected to have the following columns:
    COLUMN_NAME_CUSTOM_ITEM
    COLUMN_NAME_NUMBER_OF_IMPORTERS
    COLUMN_NAME_NUMBER_OF_AGENTS
    COLUMN_NAME_NUMBER_OF_DECLARATIONS
    COLUMN_NAME_EXTRACTED_AT_DATE
    The returned dataFrame will have the first 4 columns!
    """
    if COLUMN_NAME_EXTRACTED_AT_DATE not in existingDF:
        print("dataFrame does not contain column", COLUMN_NAME_EXTRACTED_AT_DATE, ", adding it now...")
        existingDF = existingDF.assign(extracted_at_date=None)    # <== not elegant, I have to hard-code the column name!!

    # TODO expand this condition to include items that wre scraped more than X days ago
    condition_non_processed_lines = existingDF[COLUMN_NAME_EXTRACTED_AT_DATE].isnull()  # TODO same as above
    not_processed_df_all = existingDF[condition_non_processed_lines]
    # in not_scraped_df, remove the additional columns ("Custom_Item" is index)
    # The resulting DF will contain only these 3 columns (and column "Custom_Item" which is the index)!
    not_processed_df = not_processed_df_all[[COLUMN_NAME_NUMBER_OF_IMPORTERS, COLUMN_NAME_NUMBER_OF_AGENTS, COLUMN_NAME_NUMBER_OF_DECLARATIONS]]
    return not_processed_df


def extractCustomItemsAsList(df):
    """
    df has at least the following column: COLUMN_NAME_CUSTOM_ITEM as index!
    other columns are ignored.
    :param df:
    :return:
    """
    return df.index.values.tolist()


def elicit_useful_data(unsorted_flattened_list):
    """
    [{'order': 2, 'RegularityRequirementID': '4233', 'from_item': '22257', 'from_item_fc': '1001000000', 'create_date': '2013-09-03', 'update_date': '1970-01-01', 'start_date': '2013-09-03', 'end_date': '2069-12-31', 'InceptionCodeID': '1', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '3719', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': '', 'RegularityRequiredCertificateID': '6686', 'ConfirmationTypeID': '10-0110', 'CNumber': '0', 'TextualCondition': 'כמצוין בתעריף מכס', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 5, 'RegularityRequirementID': '6112', 'from_item': '22257', 'from_item_fc': '1001000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2013-09-03', 'end_date': '2069-12-31', 'InceptionCodeID': '1', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '7256', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': '', 'RegularityRequiredCertificateID': '10618', 'ConfirmationTypeID': '10-0110', 'CNumber': '0', 'TextualCondition': '', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 18, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '8104', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 19, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '8105', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 20, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5873', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '8106', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 21, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5874', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'למאכל אדם ארוזים למכירה בקמעונאות', 'RegularityRequiredCertificateID': '8107', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 22, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '8109', 'ConfirmationTypeID': '66-0701', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 30, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8320', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '10757', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 31, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8322', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'לזריעה', 'RegularityRequiredCertificateID': '10758', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 32, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8324', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'אחרים', 'RegularityRequiredCertificateID': '10759', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 44, 'RegularityRequirementID': '5230', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2020-03-25', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '20', 'RegularityInceptionID': '8320', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '12066', 'ConfirmationTypeID': '1-0101', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'},
     {'order': 45, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5872', 'InterConditions': '1-All', 'personal': '1-Yes', 'description': 'להזנת בעלי חיים', 'RegularityRequiredCertificateID': '13149', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 46, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5874', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'למאכל אדם ארוזים למכירה בקמעונאות', 'RegularityRequiredCertificateID': '13150', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 47, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '13151', 'ConfirmationTypeID': '70-0705', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '7-משרד הבריאות'},
     {'order': 48, 'RegularityRequirementID': '2664', 'from_item': '2157', 'from_item_fc': '1000000000', 'create_date': '2016-12-15', 'update_date': '1970-01-01', 'start_date': '2016-12-15', 'end_date': '2069-12-31', 'InceptionCodeID': '2', 'RegularityPublicationCodeID': '1', 'RegularityInceptionID': '5876', 'InterConditions': '1-All', 'personal': '0-No', 'description': 'אחרים', 'RegularityRequiredCertificateID': '13152', 'ConfirmationTypeID': '2-0102', 'CNumber': '0', 'TextualCondition': ' ', 'TrNumber': '0', 'AuthorityID': '1-משרד החקלאות'}]
    :param flattened_list:
    :return:
    """
    # flattened_list.sort(key=lambda item: item['ConfirmationTypeID'].split("-")[1])    # sort in place
    flattened_list = sorted(unsorted_flattened_list, key=lambda item: item['ConfirmationTypeID'].split("-")[1])

    if len(flattened_list) == 0:
        print("no reqs")
        return [],[]

    z = [reg['end_date'] for reg in flattened_list]
    z1 = [item < '2069-12-31' for item in z]
    result = reduce(lambda x, y: x and y, z1)
    if result:
        print(z)
        print(z1)
        print(result)
        y = [reg['start_date'] + ' ' + reg['end_date'] + ' ' + reg['ConfirmationTypeID'] for reg in flattened_list]
        for item in y:
            print(item)
    # else:
    #     return

    # this prints ['1-משרד החקלאות', '7-משרד הבריאות']
    ret1 = list(set([reg['AuthorityID'] for reg in flattened_list]))
    print(ret1)

    x = list([reg['ConfirmationTypeID'] for reg in flattened_list])
    ret2 = sorted(set(x), key=second_part_of_string)
    # this prints ['1-0101', '2-0102', '10-0110', '66-0701', '70-0705']
    print(ret2)
    # for item in sorted(set(x), key=second_part_of_string):
    #     print(item)
    return ret1, ret2


def second_part_of_confirmation_id(dict1):
    x = dict1['ConfirmationTypeID']
    return x.split("-")[1]


def second_part_of_string(x):
    return x.split("-")[1]


def display(confirmers, regulations):
    print(confirmers)
    print(regulations)


def processOneItem(connection, fullClassification):
    # print("working on item", fullClassification, " ...")
    item_id = get_item_id_of_full_classification(fullClassification)
    if item_id is None:
        return []
    print("item", fullClassification,"item id:", item_id)
    flattened_list = readDB.retrieve_for_all_parents(connection, item_id)
    confirmers, regulations = elicit_useful_data(flattened_list)
    display (confirmers, regulations)
    #print(flattened_list)
    #return flattened_list # temporary
    return (confirmers, regulations)


def add_results_to_df(results, existingDF):
    df = existingDF.copy()
    # this will delete existing values in the new column if it already exists:
    df['Regulations'] = ''
    df['Confirmers'] = ''
    # the following will not add a column if it already exists, and thus will not delete existing values in that column
    # if 'Confirmers' not in existingDF.columns:
    #     df['Confirmers'] = ''
    for ind in results.keys():
        confs = []
        regs = []
        # results[ind][0] is like
        # ['1-משרד החקלאות', '7-משרד הבריאות']
        # results[ind][1] is like
        # ['1-0101', '2-0102', '10-0110', '66-0701', '70-0705']
        if len(results[ind]) > 0:
            try:
                confs = [x.split("-")[0] for x in results[ind][0]]
                regs = [x.split("-")[1] for x in results[ind][1]]
            except BaseException as err:
                print("add_results_to_df: exception", err, "ind=", ind, "results=", results[ind])
        print(confs)
        print(regs)
        #print(ind, df.at[ind, 'Number_Of_Declarations'], "a:" + str(results[ind][1]))
        df.at[ind, 'Confirmers'] = confs
        df.at[ind, 'Regulations'] = regs
        #print(ind, df.at[ind, 'Confirmers'])

    return df


def processMoreItemsAndAddToPreviousResults(existingDF):
    """
    :param existingDF:
    :return:
    """
    # print(existingDF.columns[1])
    # print('Number_Of_Agents' in existingDF.columns)
    # print('Confirmers' in existingDF.columns)
    not_processed_df = divideExistingResultsDF(existingDF)
    # not_processed_df has at least the following column:
    # COLUMN_NAME_CUSTOM_ITEM
    # other columns are ignored
    if not_processed_df is None:
        return None

    customsItemFullClassificationList = extractCustomItemsAsList(not_processed_df)
    # now the list contains ALL custom-items (actually: the FullClassification of each item) that were not processed
    print("There are", len(customsItemFullClassificationList), "items in my list")

    # now we do the equivalent of the following:
    # scrapingResults = scrapeAccordingToList(customsItemFullClassificationList, howManyItemsToScrape)
    # resulting_df = addNumberOfIshurimToDataFrame(df, scrapingResults)
    # return resulting_df

    connection = initialize_connection_and_caches()

#    processOneItem(connection, '1210100000')

    results = dict()
    #for item in customsItemFullClassificationList[:1000]:  # <== you can limit number of processed items here (for debug)
    # the full list (~7000 items) takes about 7 minutes
    for item in customsItemFullClassificationList:
        #list1, listOfIshurim = scrapeOneItem(fullClassification)
        result = processOneItem(connection, str(item))
        # result is tuple (confirmers, regulations)
        results[item] = result
        
    df = add_results_to_df(results, existingDF)
    return df


def main():
    # create_work_file() should be used ONCE, to create the file NAME_OF_RESULTS_FILE if it does not exist yet...
    # after that, do this every time:
    existingDF = read_existing_results_file()
    if existingDF is None:  # file NAME_OF_RESULTS_FILE not found
        exit(-1)
    newDF = processMoreItemsAndAddToPreviousResults(existingDF)
    if newDF is None:  # dataFrame does not contain column extracted_at_date
        exit(-2)
    write_to_excel_file(newDF)


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())

