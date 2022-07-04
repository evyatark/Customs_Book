# MySQL

## open a MySQL console in a terminal window
(according to https://stackoverflow.com/a/47814612 )

$ docker exec -it mysql_server_custom_book bash -l

you should receive a # prompt. Then:

root@03fef32f6229:/# mysql -uroot -p123456

you should receive a `mysql>` prompt. Then:

```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| my_db_1            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)
```

```
mysql> use my_db_1;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+------------------------------------+
| Tables_in_my_db_1                  |
+------------------------------------+
| AdditionRulesDetailsHistory        |
| ComputationMethodData              |
| CountriesExclusion                 |
| CustomsBookAddition                |
| CustomsBookAdditionsDetailsHistory |
| CustomsBook_Quota                  |
| CustomsItem                        |
| CustomsItemDetailsHistory          |
| CustomsItemExclusion               |
| CustomsItemLinkage                 |
| LevyCondition                      |
| LevyExclusion                      |
| PropertiesDetailsHistory           |
| QuotaDetailsHistory                |
| QuotaRenewal                       |
| RegularityInception                |
| RegularityRequiredCertificate      |
| RegularityRequirement              |
| Rule                               |
| RuleDetailsHistory                 |
| TariffDetailsHistory_777           |
| Tariff_777                         |
| TradeAgreement                     |
| TradeAgreementDetailsHistory_777   |
| TradeLevy                          |
| rStockPileData_Vendors_Vendor      |
+------------------------------------+
26 rows in set (0.00 sec)
```

To exit: `ctrl-D` twice.



## connect to MySQL from PyCharm or IntelliJ Idea
use url

jdbc:mysql://localhost:3306/my_db_1

username: evyatar_user

password: 123456

## import CSV files

I can use csvkit which is a Python package / tool:

https://csvkit.readthedocs.io/en/1.0.7/tutorial/1_getting_started.html#installing-csvkit

(best install inside a virtual env)

my ~/Documents/custom/6/pythonsql already has a virtual env (I used pyenv to create it):

```
(pysql1) evyatar@dell-precision-3551:~/Documents/custom/6/pythonsql$ pyenv local 
pysql1
(pysql1) evyatar@dell-precision-3551:~/Documents/custom/6/pythonsql$ pip install csvkit
Collecting csvkit
  Downloading csvkit-1.0.7-py2.py3-none-any.whl (42 kB)
     |████████████████████████████████| 42 kB 215 kB/s 
Collecting agate-excel>=0.2.2
  Downloading agate_excel-0.2.5-py2.py3-none-any.whl (7.1 kB)
Collecting six>=1.6.1
  Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting agate-sql>=0.5.3
  Downloading agate_sql-0.5.8-py2.py3-none-any.whl (7.1 kB)
Collecting agate>=1.6.1
  Downloading agate-1.6.3-py2.py3-none-any.whl (100 kB)
     |████████████████████████████████| 100 kB 1.3 MB/s 
Collecting agate-dbf>=0.2.2
  Downloading agate_dbf-0.2.2-py2.py3-none-any.whl (3.5 kB)
Collecting openpyxl>=2.3.0
  Downloading openpyxl-3.0.10-py2.py3-none-any.whl (242 kB)
     |████████████████████████████████| 242 kB 4.6 MB/s 
Collecting olefile
  Downloading olefile-0.46.zip (112 kB)
     |████████████████████████████████| 112 kB 10.9 MB/s 
Collecting xlrd>=0.9.4
  Downloading xlrd-2.0.1-py2.py3-none-any.whl (96 kB)
     |████████████████████████████████| 96 kB 5.4 MB/s 
Collecting sqlalchemy>=1.0.8
  Downloading SQLAlchemy-1.4.37-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.6 MB)
     |████████████████████████████████| 1.6 MB 14.1 MB/s 
Collecting Babel>=2.0
  Downloading Babel-2.10.1-py3-none-any.whl (9.5 MB)
     |████████████████████████████████| 9.5 MB 10.9 MB/s 
Collecting isodate>=0.5.4
  Downloading isodate-0.6.1-py2.py3-none-any.whl (41 kB)
     |████████████████████████████████| 41 kB 1.0 MB/s 
Collecting leather>=0.3.2
  Downloading leather-0.3.4-py2.py3-none-any.whl (31 kB)
Collecting python-slugify>=1.2.1
  Downloading python_slugify-6.1.2-py2.py3-none-any.whl (9.4 kB)
Collecting pytimeparse>=1.1.5
  Downloading pytimeparse-1.1.8-py2.py3-none-any.whl (10.0 kB)
Collecting parsedatetime!=2.5,!=2.6,>=2.1
  Downloading parsedatetime-2.4.tar.gz (58 kB)
     |████████████████████████████████| 58 kB 6.7 MB/s 
Collecting dbfread>=2.0.5
  Downloading dbfread-2.0.7-py2.py3-none-any.whl (20 kB)
Collecting et-xmlfile
  Using cached et_xmlfile-1.1.0-py3-none-any.whl (4.7 kB)
Collecting greenlet!=0.4.17; python_version >= "3" and (platform_machine == "aarch64" or (platform_machine == "ppc64le" or (platform_machine == "x86_64" or (platform_machine == "amd64" or (platform_machine == "AMD64" or (platform_machine == "win32" or platform_machine == "WIN32"))))))
  Using cached greenlet-1.1.2-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (156 kB)
Collecting pytz>=2015.7
  Using cached pytz-2022.1-py2.py3-none-any.whl (503 kB)
Collecting text-unidecode>=1.3
  Downloading text_unidecode-1.3-py2.py3-none-any.whl (78 kB)
     |████████████████████████████████| 78 kB 7.3 MB/s 
Collecting future
  Downloading future-0.18.2.tar.gz (829 kB)
     |████████████████████████████████| 829 kB 11.7 MB/s 
Building wheels for collected packages: olefile, parsedatetime, future
  Building wheel for olefile (setup.py) ... error
  ERROR: Command errored out with exit status 1:
   command: /home/evyatar/.pyenv/versions/pysql1/bin/python -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-i899dzgk/olefile/setup.py'"'"'; __file__='"'"'/tmp/pip-install-i899dzgk/olefile/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-pzq759zh
       cwd: /tmp/pip-install-i899dzgk/olefile/
  Complete output (6 lines):
  usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: setup.py --help [cmd1 cmd2 ...]
     or: setup.py --help-commands
     or: setup.py cmd --help
  
  error: invalid command 'bdist_wheel'
  ----------------------------------------
  ERROR: Failed building wheel for olefile
  Running setup.py clean for olefile
  Building wheel for parsedatetime (setup.py) ... error
  ERROR: Command errored out with exit status 1:
   command: /home/evyatar/.pyenv/versions/pysql1/bin/python -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-i899dzgk/parsedatetime/setup.py'"'"'; __file__='"'"'/tmp/pip-install-i899dzgk/parsedatetime/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-pfk00544
       cwd: /tmp/pip-install-i899dzgk/parsedatetime/
  Complete output (6 lines):
  usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: setup.py --help [cmd1 cmd2 ...]
     or: setup.py --help-commands
     or: setup.py cmd --help
  
  error: invalid command 'bdist_wheel'
  ----------------------------------------
  ERROR: Failed building wheel for parsedatetime
  Running setup.py clean for parsedatetime
  Building wheel for future (setup.py) ... error
  ERROR: Command errored out with exit status 1:
   command: /home/evyatar/.pyenv/versions/pysql1/bin/python -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-i899dzgk/future/setup.py'"'"'; __file__='"'"'/tmp/pip-install-i899dzgk/future/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-3sm2m8b9
       cwd: /tmp/pip-install-i899dzgk/future/
  Complete output (6 lines):
  usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: setup.py --help [cmd1 cmd2 ...]
     or: setup.py --help-commands
     or: setup.py cmd --help
  
  error: invalid command 'bdist_wheel'
  ----------------------------------------
  ERROR: Failed building wheel for future
  Running setup.py clean for future
Failed to build olefile parsedatetime future
Installing collected packages: et-xmlfile, openpyxl, pytz, Babel, six, isodate, leather, text-unidecode, python-slugify, pytimeparse, future, parsedatetime, agate, olefile, xlrd, agate-excel, greenlet, sqlalchemy, agate-sql, dbfread, agate-dbf, csvkit
    Running setup.py install for future ... done
    Running setup.py install for parsedatetime ... done
    Running setup.py install for olefile ... done
Successfully installed Babel-2.10.1 agate-1.6.3 agate-dbf-0.2.2 agate-excel-0.2.5 agate-sql-0.5.8 csvkit-1.0.7 dbfread-2.0.7 et-xmlfile-1.1.0 future-0.18.2 greenlet-1.1.2 isodate-0.6.1 leather-0.3.4 olefile-0.46 openpyxl-3.0.10 parsedatetime-2.4 python-slugify-6.1.2 pytimeparse-1.1.8 pytz-2022.1 six-1.16.0 sqlalchemy-1.4.37 text-unidecode-1.3 xlrd-2.0.1
(pysql1) evyatar@dell-precision-3551:~/Documents/custom/6/pythonsql$ 

```

Now use `csvsql` as explained in https://csvkit.readthedocs.io/en/1.0.7/tutorial/3_power_tools.html#csvsql-and-sql2csv-ultimate-power and https://csvkit.readthedocs.io/en/1.0.7/scripts/csvsql.html

I get error message:

```
(pysql1) evyatar@dell-precision-3551:~/Documents/custom/6/pythonsql$ csvsql --db mysql://evyatar_user:123456@localhost:3306/my_db_1 
ImportError: You don't appear to have the necessary database backend installed for connection string you're trying to use. Available backends include:

PostgreSQL:	pip install psycopg2
MySQL:		pip install mysql-connector-python OR pip install mysqlclient
```
pip install mysql-connector-python does not help - you must do 
`sudo pip install mysql-connector-python`
```
(pysql1) evyatar@dell-precision-3551:~/Documents/custom/6/pythonsql$ sudo pip install mysql-connector-python
Collecting mysql-connector-python
  Downloading mysql_connector_python-8.0.29-cp38-cp38-manylinux1_x86_64.whl (25.2 MB)
     |████████████████████████████████| 25.2 MB 4.3 MB/s 
Requirement already satisfied: protobuf>=3.0.0 in /usr/lib/python3/dist-packages (from mysql-connector-python) (3.6.1)
Installing collected packages: mysql-connector-python
Successfully installed mysql-connector-python-8.0.29
```

