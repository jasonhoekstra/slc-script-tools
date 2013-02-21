#!/usr/bin/python

import urllib2, json, csv, sys, httplib, re, pprint

def get_json(url, auth_token):
	"""Don't edit auth token here"""
	"""Specify it in command line"""
	"""Usage ./extractor.py <AUTH_TOKEN>"""
	headers = { 'Accept' : 'application/vnd.slc+json',
				'Content-Type' : 'application/vnd.slc+json',
				'Authorization' : 'bearer ' + auth_token
			  }
	try:
		if re.search('^https\:\/\/', url) or re.search('^http\:\/\/', url):
			link = ''
		else:
			link = 'https://api.sandbox.slcedu.org/api/rest/v1'

		req = urllib2.Request(link + url, None, headers)
		response = urllib2.urlopen(req)
		return response.read()
	except urllib2.HTTPError, e:
		print >>sys.stderr, 'HTTPError:', str(e)
		exit(e.errno)
	except urllib2.URLError, e:
		print >>sys.stderr, 'URLError:', str(e)
		exit(e.errno)
	except httplib.HTTPException, e:
		print >>sys.stderr, 'HTTPException', str(e)
		exit(e.errno)
	except Exception:
		import traceback
		print >>sys.stderr, 'generic exception:', traceback.format_exc()
		exit(-1)

def grade_string_to_int(grade):
	"""Transforms grade string to integer"""
	grade = grade.split()[0].lower()
	return {
		'first': 1,
		'second': 2,
		'third': 3,
		'fourth': 4,
		'fifth': 5,
		'sixth': 6,
		'seventh': 7,
		'eighth': 8,
		'nineth': 9,
		'tenth': 10,
		'eleventh': 11,
		'twelveth': 12,
		'thirteenth': 13,
		'fourteenth': 14,
	}.get(grade, 1) 


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print >>sys.stderr, "Usage :", sys.argv[0], "<AUTH_TOKEN>"
		exit(1)
	
	auth_token = sys.argv[1]

	csvfile = csv.writer(open("studentlist.csv", "wb"))

	list = []

	list.append("SIS_ID")
	list.append("SLC_ID")
	list.append("FIRST_NAME")
	list.append("MIDDLE_NAME")
	list.append("LAST_NAME")
	list.append("GENDER_MALE")
	list.append("GENDER_FEMALE")
	list.append("USER_NAME")
	list.append("GRADE")
	list.append("SCHOOL_NAME")
	list.append("SECTION_TITLE")

	csvfile.writerow(list)

	list = []
	
	teachers = json.loads(get_json('/teachers', auth_token))
	for teacher in teachers:
		for link in teacher['links']:
			if link['rel'] == 'getTeacherSectionAssociations':
				lk = link['href']
				break

		sections = json.loads(get_json(lk, auth_token))

		for section in sections:
			links = section['links']
			for link in links:
				if link['rel'] == 'getSection':
					lk = link['href']
					break

			section_title = json.loads(get_json(lk, auth_token))['uniqueSectionCode']

			links = json.loads(get_json(lk, auth_token))['links']
			for link in links:
				if link['rel'] == 'getStudents':
					lk = link['href']
					break			

			students = json.loads(get_json(lk, auth_token))
		
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

				"""USER_NAME"""
				list.append(student["name"]["firstName"].lower() + '_' + student["name"]["lastSurname"].lower())
				
				"""Grade and School name"""
				student_extra = json.loads(
					get_json('/students/'+ student["id"] +'/studentSchoolAssociations', auth_token)
				)
				list.append(grade_string_to_int(student_extra[0]['entryGradeLevel']))

				school = json.loads(
					get_json('/schools/'+ student_extra[0]['schoolId'], auth_token)
				)

				list.append(school['nameOfInstitution'])
				try:
					list.append(section_title)
				except:
					pass
				
				csvfile.writerow(list)
				print list
				list = []
