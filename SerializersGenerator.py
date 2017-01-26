import re, copy
from field import Field

'''
The serialzerGenerator does not work for Depth and some Parameters
'''

def generateSerializer(models, appName):
	""" Create Serializer
	Parem: models, appName
	models = dictionary of each model. The name of the model is the key linked to Field Object
	appName = Application name
	"""

	# create import statements
	output = open("result/serializers.py","w+")
	output.write("from rest_framework import serializers\n")
	output.write("from "+ appName + ".models import ")
	for index, model in enumerate(models, start=0):
		if index == 0:
			output.write(model)
		else :
			output.write(", "+model)
	output.write("\n\n")

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
	for model in models:

		fields = models[model]
		foreignKeyFields = []
		primaryKey = ""
		for field in fields:
			fieldObject = fields[field]
			if fieldObject.isForeignKey:
				foreignKeyFields.append(fieldObject)
			if fieldObject.isPrimaryKey:
				primaryKey = fieldObject.name

		# Writing a simple serializer
		output.write("class "+model+"Serializer(serializers.ModelSerializer):\n\n")
		output.write("\tclass Meta:\n")
		output.write("\t\tmodel = "+model+"\n")
		output.write("\n")
		# Writing a nested serializer
		if foreignKeyFields:
			output.write("class "+model+"NestedSerializer(serializers.ModelSerializer):\n\n")
			output.write("\tclass Meta:\n")
			output.write("\t\tmodel = "+model+"\n")
			# output.write("\t\texclude = ('"+primaryKey+"',)\n")
			output.write("\t\tdepth = 1\n")
			output.write("\n")
