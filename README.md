# TFNTEST

This is  project developed on django to complete developer test required for dev and ops teams.

## Table of Contents
* [instalation](#instalation)
* [api docs](#api_docs)
* [audit](#audit)
* [reporting](#reporting)


# Instalation: <a name="instalation"></a>
to instalate the software good practice of python virtual environment must be followed,
once the virtual environment has been setted up execute:
```shell
# this will install all the required libraries for the software
$ pip install -r requirements

# this command will create the needed tables, indexes and relations on database
$ python manage.py migrate

# this command will populate tables with basic dummy data
$ python manage.py shell < setup.py
```

# API Docs: <a name="api_docs"></a>
For your convenience a documentation for each endpoint of the API is provided on the following 
[link](https://documenter.getpostman.com/view/11257528/UVkiRdR6). This is a link to Postman like documentation 
which includes request and response examples with their methods and status codes.

# Audit: <a name="audit"></a>
Since a requirement about auditing was included on details, 
a sql Oracle type file containing a table and a trigger creation is provided, 
this was made this way because the database used for development was sqlite.

# Reporting: <a name="reporting"></a>
A report tool was provided to extract documents or address data:
```shell
# this argument will display the help provided inside the tool
$ python report.py --help
usage: Report [-h] [--out-file OUT_FILE] [--extract {documents,addresses}]

optional arguments:
  -h, --help            show this help message and exit
  --out-file OUT_FILE   file to output result
  --extract {documents,addresses}
                        information to extract

# this argument will let the tool extract all documents data for users
$ python report.py --extract=documents
$ cat report.csv
"userid","names","last_names","id","type","value"
"1","new names","Gomez","1","DUI","00000000-0"
"1","new names","Gomez","3","DUI","000000"
"2","Francisco","Gomez","2","NIT","0000-000000-000-0"

# this argument will let the tool extract all addresses data for users
$ python report.py --extract=addresses
$ cat report.csv 
"userid","names","last_names","id","type","value"
"1","new names","Gomez","3","HOME","lives on his house"
"2","Francisco","Gomez","2","WORK","88 y 85 Av"

# this argument will let the tool extract all addresses data for users and save that data to the given file
$ python report.py --extract=addresses --out-file=addresses.csv
$ cat report.csv 
"userid","names","last_names","id","type","value"
"1","new names","Gomez","3","HOME","lives on his house"
"2","Francisco","Gomez","2","WORK","88 y 85 Av"
```