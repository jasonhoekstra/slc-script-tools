#!/usr/bin/python

import urllib2, json, csv

headers = { 	'Accept' : 'application/vnd.slc+json',
				'Content-Type' : 'application/vnd.slc+json',
				'Authorization' : 'bearer YOUR_API_TOKEN'
		  }

req = urllib2.Request('https://api.sandbox.slcedu.org/api/rest/v1/students', None, headers)
response = urllib2.urlopen(req)
jsonresponse = response.read()

students = json.loads(jsonresponse)

#### print students """
##print 'INDENT:', json.dumps(students, sort_keys=True, indent=2)

csvfile = csv.writer(open("studentlist.csv", "wb"))

list = []

list.append("SIS_ID")
list.append("SLC_ID")
list.append("FIRST_NAME")
list.append("MIDDLE_NAME")
list.append("LAST_NAME")
list.append("GENDER_MALE")
list.append("GENDER_FEMALE")

csvfile.writerow(list)

list = []

for student in students:
	list.append(student["studentUniqueStateId"])
	list.append(student["id"])
	list.append(student["name"]["firstName"])
	if "middleName" in student["name"]:
		list.append(student["name"]["middleName"])
	else:
		list.append("")
	list.append(student["name"]["lastSurname"])
	if student["sex"] == "Male":
		list.append("Y")
	else:
		list.append("N")
	if student["sex"] == "Female":
		list.append("Y")
	else:
		list.append("N")	

	csvfile.writerow(list)
	print list
	list = []
    

