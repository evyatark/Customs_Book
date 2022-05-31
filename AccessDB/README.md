# AccessDB

Reading and converting an AccessDB file to a MySQL database

## Background
The Israeli customs web-site [Shaar-Olami](https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/CustomsTaarifEntry) exports its data as a series of XML files, and as an accdb file.

Downloading the files can be accessed [here](https://www.gov.il/he/service/2customs-tariff) (the links at the bottom left), or use the [direct link (WARNING a large RAR file!)](https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Home/DownloadFile)

The accdb file can be opened with a Microsoft Office Access DB (on a Windows OS). However, to make it more accessible for programmatical queries (and for non-Windows users), I convert this file to a MySQL database.

Note: I could convert to any other form of an SQL database, e.g. PostgreSQL.

## Method
I use Java code that reads the accdb file and creates a text file containing INSERT statements. This text file can then be "imported" by a MySQL client into a MySQL database.

In general the INSERT statements could be imported to any other SQL database (e.g. PostgreSQL), but the SQL syntax is a bit different for each database. Currently the SQL syntax requires a MySQL database.

I started with code from [AccessConverter](https://github.com/clytras/AccessConverter).
It works fine for small databases, but has some memory issues with my 1.1GB accdb file.
So I changed some parts of the code. Therefore I put here the Full code base.

## Converting accdb file
For detailed explanation of my code, see [here](documentation.md)

## Importing the resulting SQL file(s)
In general you need to install and run a MySQL database server on your computer, then install a MySQL client and use it from command line to import the SQL file(s).

I use docker to run the MySQL server, and another docker to run the MySQL client (It requires some basic knowledge of Docker, but the advantage is that I do not need to install MySQL on my machine!)
This could also be achieved with a docker-compose (like in the OpenBus Stride project).

## Additional required tables
Some of the values in some of the tables are codes that refer to "System tables" available in Shaar-Olami web-site [here](https://www.gov.il/apps/taxes/systemtable/). I would need to create an SQL import file for these tables, but this requires adifferent code (because the system tables can be downloaded in Excel format only, not as accdb)