# import os
import pandas as pd
import datetime

'''
Fix Importers file
------------------
Assumes an Excel file "importers.xlsx" with its first tab containing data that needs to be fixed.
Ignores the other tabs!
Creates a new Excel file (named by default "temp1.xlsx") with 2 tabs named "original", "processed".
The "processed" tab contains same data but with additional lines:
wherever in original tab the 4th column contains several numbers split by ','
 the processed tab contains several lines, in each of them the 4th column has one of the numbers
Processing is slow because we iterate line by line. For 80,000 lines takes about X minutes.
'''

FILENAME : str = 'importers.xlsx'
PROCESSED_COLUMN_NUM : int = 3  # if val is 3, the 4th column will be processed


def write_to_excel_file(df, out_file_name = "temp1.xlsx"):
    excel_file = pd.ExcelWriter(out_file_name)
    df.to_excel(excel_writer=excel_file, sheet_name="items", index=True)
    excel_file.save()


def write_both_to_excel_file(df_orig, df_processed, out_file_name = "temp1.xlsx"):
    excel_file = pd.ExcelWriter(out_file_name)
    df_orig.to_excel(excel_writer=excel_file, sheet_name="original", index=True)
    df_processed.to_excel(excel_writer=excel_file, sheet_name="processed", index=True)
    excel_file.save()


def insert_lines(df, df_out, max_number_of_lines = -1):
    number_of_lines = df.shape[0]
    new_ind = 0
    if max_number_of_lines > 0:
        number_of_lines = min(max_number_of_lines, df.shape[0])
    else:
        number_of_lines = df.shape[0]

    for index in range(number_of_lines):
        content = str(df.iat[index, PROCESSED_COLUMN_NUM])
        if ',' in content:
            print(index, ':', content)
            vals = content.split(sep=',')
            for val in vals:
                df_out.loc[new_ind] = df.loc[index]
                df_out.iat[new_ind, PROCESSED_COLUMN_NUM] = int(val)
                new_ind = new_ind + 1
        else:
            df_out.loc[new_ind] = df.loc[index]
            new_ind = new_ind + 1
    print(df_out.shape)
    return df_out


def process_excel_file(filename):
    """
    From the specified Excel file (it would normally be "importers.xlsx"),
     read ONLY the data in FIRST tab!
    :param filename: name of the source file. Could be full path, otherwise it is assumed to be in current directory.
    :return: nothing! creates a new Excel file on file system!!
    """
    # df_out = pd.DataFrame(columns=['lib', 'qty1', 'qty2'])
    # for i in range(5):
    #     df_out.loc[i] = ['aaa', 'bbb', 'ccc']
    # print(df_out)

    df = pd.read_excel(filename, sheet_name=0)
    # print(df.tail(40))

    # this prints first line (actually second line in the file because first line is headers!)
    # print(df.iat[0,0])
    # print(df.iat[0,1])
    # print(df.iat[0,2])
    # print(df.iat[0,3])
    # print('\n\n')

    # this prints all of first line
    print(df.iloc[1])
    print('\n\n')

    df_out = pd.DataFrame(columns=df.columns)
    # df.shape returns tuple (85790, 4)
    # df.iat[7, 3] is the number(s) in line 7, column 3

    # df_out = insert_lines(df, df_out, 200)
    df_out = insert_lines(df, df_out)

    print(df_out.shape)

    print(df_out)
    # write_to_excel_file(df_out)
    write_both_to_excel_file(df, df_out)


def main():
    # read_excel_file(os.getcwd() + '/' + FILENAME)
    process_excel_file(FILENAME)


if __name__ == "__main__":
    startedAt = datetime.datetime.now()
    main()
    print('started at', startedAt)
    print('completed at', datetime.datetime.now())
