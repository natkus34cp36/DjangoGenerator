# models {
# 	"Model1" : {
# 		"Field1" : Field_Object,
# 		"Field2" : Field_Object,
# 	},{
# 	"Model2" :
# 		"Field1" : Field_Object,
# 		"Field2" : Field_Object,
# 	},
# }

import re, copy
import ModelGenerator
from field import Field


def getFieldsFromFile(fileName):
	justStarted = True
	tableName = ""
	models = {}
	fields = {}

	with open(fileName, 'r') as readFile:
		content = readFile.readlines()
		count = 0
		for index, contentLine in enumerate(content, start=0):
			elements = contentLine.split()
			print "elements", index, elements, count
			unprocessed = {"INDEX", "PRIMARY"}

			# check the first word in each line
			if elements[0] == "CREATE":
				count = 0
				if justStarted:
					tableName = elements[5][elements[5].find(".") + 1:]
					justStarted = False
				else:
					models[tableName] = copy.deepcopy(fields)
					tableName = elements[5][elements[5].find(".") + 1:]

				fields = {}
			elif elements[0] == "INDEX":
				continue
			elif elements[0] == "PRIMARY":
				for x in elements[2:]:
					y = x.replace("(", "")
					y = y.replace(")", "")
					y = y.replace(",", "")
					print y
					fields[y].isPrimaryKey = True
			elif elements[0] == 'CONSTRAINT':
				line1 = content[index]
				line2 = content[index + 1]
				line3 = content[index + 2]
				line4 = content[index + 3]
				line5 = content[index + 4]
				# print line1, line2, line3, line4, line5
				foreign_key = line2.split()[2][1:-1]
				to_table = line3.split()[1]

				indexOfDot = to_table.find(".") + 1
				to_table = to_table[indexOfDot:]

				fields[foreign_key].isForeignKey = True
				fields[foreign_key].to_table = to_table
			elif elements[0] == 'UNIQUE':
				field_name = elements[2]
				indexOfUnderScore = elements[2].find("/")
				field_name = field_name[:indexOfUnderScore]
				fields[field_name].isUnique = True
			else:
				name = elements[0]
				field_type = elements[1]
				nullable = elements[2]
				nullable = nullable.replace(",", "")

				# handle default value in "int", "float" and "varchar"
				defaultValue = None
				defaultIndex = 2
				if nullable == "NULL":
					defaultIndex += 1
				else: # "not null"
					defaultIndex += 2
				if defaultIndex < len(elements) and elements[defaultIndex] == "DEFAULT":
					# check until COMMENT or end
					firstDefault = 1
					defaultValue = ""
					defaultIndex += 1

					while defaultIndex < len(elements) and elements[defaultIndex] != "COMMENT":
						if firstDefault:
							defaultValue += elements[defaultIndex]
							firstDefault = 0
						else:
							defaultValue += " " + elements[defaultIndex]
						defaultIndex += 1


				# print defaultValue
				if defaultValue is not None and defaultValue.endswith(','):
					defaultValue = defaultValue[0:len(defaultValue)-1]

				# Start filling in fields
				if field_type.startswith("VARCHAR"):
					# print "Adding " + name,field_type,nullable
					firstIndex = field_type.find("(")
					secondIndex = field_type.find(")")
					length = field_type[firstIndex + 1:secondIndex]
					if nullable == "NULL":
						fields[name] = Field(name, "VARCHAR", length, True, count, defaultValue)
					else:
						fields[name] = Field(name, "VARCHAR", length, False, count, defaultValue)
				elif field_type == "INT":
					# print "Adding " + name,field_type,nullable
					# defaultValue = int(defaultValue) if defaultValue else None
					if nullable == "NULL":
						fields[name] = Field(name, "INT", None, True, count, defaultValue)
					else:
						fields[name] = Field(name, "INT", None, False, count, defaultValue)
				elif field_type == "FLOAT":
					# print "Adding " + name,field_type,nullable
					# defaultValue = float(defaultValue) if defaultValue else None
					if nullable == "NULL":
						fields[name] = Field(name, "FLOAT", None, True, count, defaultValue)
					else:
						fields[name] = Field(name, "FLOAT", None, False, count, defaultValue)
				elif field_type == "TINYINT(1)":
					# print "Adding " + name,field_type,nullable
					# defaultValue = int(defaultValue) if defaultValue else None
					if nullable == "NULL":
						fields[name] = Field(name, "BOOLEAN", None, True, count, defaultValue)
					else:
						fields[name] = Field(name, "BOOLEAN", None, False, count, defaultValue)
				elif field_type.startswith("TEXT"):
					firstIndex = field_type.find("(")
					secondIndex = field_type.find(")")
					length = field_type[firstIndex + 1:secondIndex]
					if nullable == "NULL":
						fields[name] = Field(name, "TEXT", length, True, count, defaultValue)
					else:
						fields[name] = Field(name, "TEXT", length, False, count, defaultValue)
				elif field_type == "DATETIME":
					if nullable == "NULL":
						fields[name] = Field(name, "DATETIME", None, True, count, defaultValue)
					else:
						fields[name] = Field(name, "DATETIME", None, False, count, defaultValue)
				elif field_type == "DATE":
					if nullable == "NULL":
						fields[name] = Field(name, "DATE", None, True, count, defaultValue)
					else:
						fields[name] = Field(name, "DATE", None, False, count, defaultValue)
				else:
					continue
				count += 1

		models[tableName] = copy.deepcopy(fields)
		printModels(models)
	return models


def printModels(models):
	i = 1
	for model in models:
		print model
		for field in models[model]:
			print  str(i) + ": " + str(models[model][field])
			i += 1
		print "------------------------------"
		i = 1
