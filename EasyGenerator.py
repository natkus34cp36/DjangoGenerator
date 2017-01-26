import re, copy
from field import Field

def generateEasy(models):
	output = open("result/mars.txt","w+")

	for model in models:
		model_name = model
		output.write("\n")
		output.write("MODEL: "+model_name+"\n")
		output.write("\n")
		output.write("_____________________LIST VIEW_____________________\n\n")
		fields = models[model]
		for count in range(0, len(fields)):
			for field in fields:
				if count == fields[field].index :
					fieldObject = fields[field]
					output.write(fieldObject.name+"\n")
		output.write("\n")

		output.write("_______________________ CSV _______________________\n\n")
		fields = models[model]
		length = 0
		lengthLimit = 70
		for count in range(0, len(fields)):
			for field in fields:
				if count == fields[field].index :
					fieldObject = fields[field]
					if count == len(fields)-1:
						length += len(str(fieldObject.name))
						if length > lengthLimit:
							output.write("\n")
							length = 0
						output.write(fieldObject.name+"\n")
					else :
						length += len(str(fieldObject.name))
						if length > lengthLimit:
							output.write("\n")
							length = 0
						output.write(fieldObject.name + ",")
		output.write("\n\n")

		output.write("__________________ CSV with Quote __________________\n\n")
		fields = models[model]
		length = 0
		lengthLimit = 70
		output.write("[")
		for count in range(0, len(fields)):
			for field in fields:
				if count == fields[field].index :
					fieldObject = fields[field]
					if count == len(fields)-1:
						length += len(str(fieldObject.name))
						if length > lengthLimit:
							output.write("\n")
							length = 0
						output.write("'"+fieldObject.name+"'"+"\n")
					else :
						length += len(str(fieldObject.name))
						if length > lengthLimit:
							output.write("\n")
							length = 0
						output.write("'"+fieldObject.name+"'" + ",")
		output.write("]")
		output.write("\n\n")

		output.write("____________________ OnChange _____________________\n\n")
		fields = models[model]
		for count in range(0, len(fields)):
			for field in fields:
				if count == fields[field].index :
					fieldObject = fields[field]
					output.write("this.props.fields."+fieldObject.name+".onChange("+fieldObject.name+");\n")
		output.write("\n")

		output.write("__________________ End of "+model_name+"__________________\n\n\n\n")
