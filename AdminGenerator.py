import re, copy
from field import Field

def generateAdmin(models, appName):
	output = open("result/admin.py","w+")

	output.write("from django.contrib import admin\n")
	output.write("from "+appName+".models import ")
	for index, model in enumerate(models, start=0):
		if index == 0:
			output.write(model)
		else :
			output.write(", "+model)
	output.write("\n\n")

	for model in models:
		output.write("admin.site.register(" + model + ")\n")
	output.write("\n")