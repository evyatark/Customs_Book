# Customs_Book
ספר היבוא והמכס

This python script reads an Excel file, then it uses Web Scraping of the ShaarOlami web-site to read data from the web-site. Then it parses that data and counts for each customsItem, how many permissions it requires.

# Working with Python, BeautifulSoup, Pandas, Excel

## Preparing
create a virtual env (only the first time) and activate it

```
cd work/python/pandas3/
pyenv virtualenv pandas3
pyenv activate pandas3

(pyenv virtualenvs)

pip3 install pandas
pip3 install openpyxl xlrd

pip3 install BeautifulSoup4
```

## Warnings!
This script uses web-scraping to read from a web site. You must restrict the load on the web-site!

Currently this is done by reading only `NUMBER_OF_ITEMS_TO_SCRAPE` items.

In general it could also be restricted by controlling the rate of requests to the site.

## Executing Python script
After editing the file `readExcel.py`, run it:

```
python readExcel.py
```


## Working with Pandas
see [this](./Pandas_Documentation.md) document.

