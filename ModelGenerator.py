import re, copy
from field import Field


def generateModel(models):
	output = open("result/models.py", "w+")
	output.write("from __future__ import unicode_literals\n")
	output.write("from django.db import models\n")
	output.write("from datetime import date\n\n")

	for model in models:
		model_name = model
		output.write("class " + model_name + "(models.Model):\n")
		fields = models[model]
		for count in range(0, len(fields)):
			for field in fields:
				if count == fields[field].index:
					firstAttribute = 1  # to check if need comma or not

					fieldObject = fields[field]
					print fieldObject
					output.write("\t" + fieldObject.name + " = models.")

					# create the field object
					if fieldObject.isForeignKey:
						output.write("ForeignKey(\"" + fieldObject.to_table + "\", on_delete=models.PROTECT, db_column = '"+fieldObject.name+"'")
						firstAttribute = 0
					else:
						if fieldObject.field_type == "VARCHAR":
							output.write("CharField(max_length=" + str(fieldObject.length))
							firstAttribute = 0
						elif fieldObject.field_type == "INT":
							if fieldObject.isPrimaryKey:
								output.write("AutoField(primary_key=True")
								firstAttribute = 0
							else:
								output.write("IntegerField(")
						elif fieldObject.field_type == "FLOAT":
							output.write("FloatField(")
						elif fieldObject.field_type == "BOOLEAN":
							# output.write("BooleanField(default=False")
							output.write("BooleanField(")
						elif fieldObject.field_type == "TEXT":
							output.write("TextField(")
						elif fieldObject.field_type == "DATETIME":
							# auto_now_add is for updateTime, for createTime should be auto_now
							output.write("DateTimeField(auto_now_add=True")
							firstAttribute = 0
						elif fieldObject.field_type == "DATE":
							output.write("DateField(default=date.today")
							firstAttribute = 0

					hasDefault = 0
					# create the options for the fields
					if fieldObject.isUnique:
						if firstAttribute == 1:
							output.write("unique=True")
							firstAttribute = 0
						else:
							output.write(", unique=True")
					if fieldObject.default is not None and fieldObject.field_type != "DATETIME" and fieldObject.field_type != "DATE":
						hasDefault = 1
						if firstAttribute == 1:
							output.write("default=" + fieldObject.default)
							firstAttribute = 0
						else:
							output.write(", default=" + fieldObject.default)
					if fieldObject.nullable:
						if firstAttribute == 1:
							output.write("null=True")
							firstAttribute = 0
						else:
							output.write(", null=True")
					elif not fieldObject.nullable and hasDefault == 0:
						if firstAttribute == 1:
							output.write("null=False")
							firstAttribute = 0
						else:
							output.write(", null=False")

					# close option by ) and \n
					output.write(")\n")

		output.write("\n")
		output.write("\tclass Meta:\n")
		output.write("\t\tdb_table = '"+model_name+"'\n")
		output.write("\n")
