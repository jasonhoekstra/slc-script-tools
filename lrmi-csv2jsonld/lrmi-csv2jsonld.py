#!/usr/bin/python

import json, sys, csv, re

def write_json_file(json_string, file_path):
	"""
	Write json string to file
	"""
	print file_path
	try:
		f = open(file_path, 'w+')
		f.write(json_string)
	except IOError, e:
		print >>sys.stderr,e
		exit(e.errno)

def strip_list_values(array):
	"""
	trims all values in a list
	"""
	for index in range(len(array)):
		try:
			array[index] = array[index].strip()
		except:
			array[index] = strip_list_values(array[index])
	return array


def process_json_list(array):
	"""
	transforms values to lists
	"""
	for index in range(len(array)):
		array[index] = array[index].split(',')
	return array

def make_json(row, heading, index):
	"""
	converts a string line into JSON
	"""
	row = process_json_list(row)
	row = strip_list_values(row)
	json_tuple = {}
	
	complex_fields_tuple = {}
	complex_headings = []

	"""Initialize schema types"""
	schema_types = {\
		'educationalAlignment': 'http://schema.org/AlignmentObject',\
		'author': 'http://schema.org/Person',\
		'video': 'http://schema.org/VideoObject',\
		'publisher': 'http://schema.org/Organization',\
	}

	"""Identify hields"""
	for i, field_name in enumerate(heading):
		json_tuple[field_name] = row[i]

		if re.match(r"(.*)_[0-9]?_(.*)", field_name) and row[i] != [""]:
			complex_headings.append(field_name)
			exploded_field_name = field_name.split('_')
			exploded_field_name[1] = int(exploded_field_name[1]) - 1
			try:
				x = complex_fields_tuple[exploded_field_name[0]]
			except:
				complex_fields_tuple[exploded_field_name[0]] = {}
			try:
				x = complex_fields_tuple[exploded_field_name[0]][exploded_field_name[1]]
			except:
				complex_fields_tuple[exploded_field_name[0]][exploded_field_name[1]] = {}
				
			complex_fields_tuple[exploded_field_name[0]][exploded_field_name[1]][exploded_field_name[2]] = json_tuple[field_name]

	json_final_tuple = {\
		'type': [u'http://schema.org/CreativeWork']\
	}

	json_final_tuple['properties'] = {}
	
	"""Simple properties"""
	for i,h in enumerate(list(set(heading) - set(complex_headings) - set([""]))):
		if json_tuple[h] != [""]:
			if h == 'id':
				json_final_tuple['properties'][h] = json_tuple[h][0]
			else:
				json_final_tuple['properties'][h] = json_tuple[h]
		
	
	"""complex properties"""
	
	for i,p in enumerate(complex_fields_tuple):
		try:
			schema_type = schema_types[p]
		except:
			print >>sys.stderr,"Schema type is not defined:",p
			print >>sys.stderr,"Assuming typeless"
			schema_type = ""
		
		try:
			x = json_final_tuple['properties'][p]
		except:
			json_final_tuple['properties'][p] = []

		"""retrieve sub elements"""
		for j,e in enumerate(complex_fields_tuple[p]):
			try:
				x = json_final_tuple['properties'][p][e]
			except:
				json_final_tuple['properties'][p].append({})

			if schema_type != "":
				json_final_tuple['properties'][p][e]['type'] = [schema_type]

			try:
				x = complex_fields_tuple[p][e]['id']
				if x != [""]:
					json_final_tuple['properties'][p][e]['id'] = complex_fields_tuple[p][e]['id'][0]
			except:
				pass

			"""Properties"""
			for k,f in enumerate(complex_fields_tuple[p][e]):
				try:
					x = json_final_tuple['properties'][p][e]['properties']
				except:
					json_final_tuple['properties'][p][e]['properties'] = {}

				if f != 'id':	
					try:
						x = json_final_tuple['properties'][p][e]['properties'][f]
					except:
						json_final_tuple['properties'][p][e]['properties'][f] = []
					json_final_tuple['properties'][p][e]['properties'][f] = complex_fields_tuple[p][e][f]

	write_json_file(json.dumps(json_final_tuple, indent=4), 'file'+str(index)+".json")

def csv2json(file_name):
	"""
	creates JSON files from a given CSV file
	"""
	try:
		file_handle = open(file_name,'rU')
		reader = csv.reader(file_handle, dialect='excel')
		
		try:
			for i, row in enumerate(reader):
				"""get heading"""
				if i == 0:
					heading = row
				else:
					try:
						make_json(row, heading, i)
					except IndexError, e:
						print >>sys.stderr,"Invalid row:",i
						print >>sys.stderr,e
		except:
			print >>sys.stderr,"Input file does not seam do be a valid CSV"
			exit(-1)
			

	except IOError, e:
		print >>sys.stderr,e
		exit(e.errno)
		

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print >>sys.stderr,"Usage :",sys.argv[0],"<CSV>"
		exit(1)
	
	csv2json(sys.argv[1])

