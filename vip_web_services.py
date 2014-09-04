#How to run the web service
# 1. First you will need to open port 8080 on your AWS instance
#    For that you will need to go to the security groups, find the 
#	 right group that your instance is using, edit the group and add
#	 custom TCP rule with port 8080 and for the source using anywhere
#
# 2. In the command line run python mongodb_bottle_example.py
#    Notice that this will block your command line and you can no
#    longer use it unless you terminate the web service.
#
#	 Alternatively, you can run the web service in the background as follows:
#	 nohup mongodb_bottle_example.py &
#
# 3. Go to your browser and try it. In the address bar type:
#    xxx.xxx.xxx.xxx:8080/    this is the base URI
#    
#    xxx.xxx.xxx.xxx is your AWS instance IP address

#import the mongodb package
from pymongo import MongoClient

#import bottle
from bottle import route, run, template, response

#import JSON so we can covert python dictionary to JSON 
import json

#in web services / defines the base of the web service
#usually the base does not provide anything meaninguful 
#but we have to define it
#
#all routes have to conform to FHIR API standards, you cannot
#just give your route whatever name you feel like
#
#the web service provides resources (URIs) those URIs are also
#called routes. So you will notice that for every API function 
#such index, we will have to provide a route
#
#the route defines how to access that resource.
#Example: suppose your AWS instance IP address is xxx.xxx.xxx.xxx
#then once you run the web service you can go to the browser and in the
#address bar type xxx.xxx.xxx.xxx:8080/
#
#OK, why are we using port 8080? Simple. Our AWS instance is running the apache 
#web server on port 80. So the port is in use. Therefore we have 
#to use another HTTP port like 8080
@route('/')
def index():
	return "Hello, this is the VIP class web service"

#this route will get all patient information
#this route is not based on FHIR
@route('/patients')
def get_patients_info():
	#make sure the content type is set to JSON
	response.content_type = "application/json"

	#connect to mongoDB
	client = MongoClient("localhost", 27017)
	db = client.vip

	#this is an empty array that will hold all patients
	#it is an array of patient dictionaries
	docs = []

	for doc in db.patients.find({},{'_id':False,"birthDate":False}):
		#append patient to dictionary
		docs.append(doc)

	#convert dictionary to JSON
	return json.dumps(docs)

#the run command will start running the web service one you run this script in
#the command line
#notice that the host is 0.0.0.0 instead of your IP address, this tells the web
#service to serve the content to any machine/computer
run(host="0.0.0.0",port=8080)
