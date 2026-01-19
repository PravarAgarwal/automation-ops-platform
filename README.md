the end to end flow is somewhat interesting:

Client JSON
|
v
JobCreate (validate input)
|
v
Business Logic
|
v
Job Model (DB)
|
v
JobResponse (serialize output)
|
v
JSON Response

initially
we started by creating our config file, after that we created our database file, database file imported data fixed data like dB URL from config file, the database file contains the logic to for engine creation (the way through which FastAPI will interact with the database),
session factory is also created in it (session to use db for various bussiness logic purposes)

base ORM class is also initiated in this file.

after that we created our models file which contains the type of data that is required to be stored in the database.
the data class that is defined in this file will inherit from the base class that we initiated in the database.py file.

Important Note related to sessions:
Session is a class that is imported from SQLAlchemy.orm
LocalSession is a callable object that is being made with the help of sessionmaker, sessionmaker is like a session factory
when get db function creates a db instance by calling LocalSession(), it is esentially creating a Session object. This session object helps linking FastAPI with the dB.
