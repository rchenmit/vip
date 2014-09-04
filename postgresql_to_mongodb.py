#this script will demonstrate how to pull data from PostgreSQL and insert
#it into mongoDB

from pymongo import MongoClient
import psycopg2
import sys
import numpy as np
import pandas as pd

""" Pull data from PostgreSQL
This section will show a simple example on how to pull patient data
from MIMIC2 database stored in PostgreSQL
"""
#PostgreSQL username and database name (you do not need to change those):
username = 'ubuntu'
dbname = 'MIMIC2'

#connect to the database; throw an exception if database cannot be accessed for some reason
try:
    conn = psycopg2.connect(database = dbname, user=username)
    print "successfully connected to psql db!"
except:
    print "ERROR: I am unable to connect to the database!"
    sys.exit()

#cursor;
cur = conn.cursor()
try:
    cur.execute("SELECT subject_id, sex, dob from d_patients limit 25") #type the SQL query in here. 
except:
    print "I cannot SELECT names"

""" Tranform data from PostgreSQL to mongoDB
once we have connected to the PostgreSQL database successfully we can go ahead
and connect to mongoDB
"""

#this will connect to mongoDB on port 27017
client = MongoClient("localhost", 27017)

#here we will use a database called vip, if it does not exist it will get created
db = client.vip

#now we will create a new collection in the vip database called patients
patients = db.patients

#fetch rows from PostgreSQL query
#each row contains 3 columns: subject_id, sex, dob
rows = cur.fetchall()

for row in rows:
    #foreach row create a python dictionary that represents basic patient
	#information. the dictionary is like JSON format
	#this dictionary should have the same format and field names as FHIR
    patient = {"identifier":row[0],"gender":row[1],"birthDate":row[2]}

	#insert the patient into the patients collections
    patients.insert(patient)
