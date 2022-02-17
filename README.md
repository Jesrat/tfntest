# TFNTEST

This project was developed on django to complete developer test required for dev and ops teams.

## Table of Contents
* [instalation](#instalation)
* [api docs](#api_docs)
* [audit](#audit)
* [reporting](#reporting)


# Instalation: <a name="instalation"></a>
To instalate the software good practice of python virtual environment should be followed, and python should be installed 
on the host machine, in order to download python please refer to their home page for [download](https://www.python.org/downloads/).

To create the virtual environment for isolate all project libraries from the ones that already exists on the host machine
please follow the official [documentation](https://docs.python.org/3/library/venv.html).

Once the virtual environment has been setted up execute the following commands on the chosen working dir:
```shell
# this command will fetch all the project files
$ git clone https://github.com/Jesrat/tfntest.git

# this command will install all the required libraries for the project
$ pip install -r requirements

# this command will create the required tables, indexes and relations on database
$ python manage.py migrate

# this command will populate tables with basic dummy data
$ python manage.py shell < setup.py

# this command will run the builtin webserver from django
$ python manage.py runserver 0:8000
```

# API Docs: <a name="api_docs"></a>
For your convenience a documentation for each endpoint of the API is provided on the following 
[link](https://documenter.getpostman.com/view/11257528/UVkiRdR6). This is a link to Postman like documentation 
which includes request and response examples with all their methods and status codes.

# Audit: <a name="audit"></a>
Since a requirement about auditing was included on details, 
an Oracle type sql file containing the creation of an audit table and creation of all needed triggers is provided, 
it was made this way because the database used for development was sqlite.

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