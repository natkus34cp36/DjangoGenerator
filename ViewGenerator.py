import re, copy
from field import Field

def generateView(models):
	output = open("result/views.py","w+")

	output.write("from models import ")
	for index, model in enumerate(models, start=0):
		if index == 0:
			output.write(model)
		else :
			output.write(", "+model)
		
	output.write("\n")

	output.write("from serializers import ")
	for index, model in enumerate(models, start=0):
		# check if it has a foreignkey
		fields = models[model]
		foreignKeyFields = []
		for field in fields:
			fieldObject = fields[field]
			if fieldObject.isForeignKey:
				foreignKeyFields.append(fieldObject)

		if index == 0:
			output.write(model+"Serializer")
		else :
			output.write(", "+model+"Serializer")

		if foreignKeyFields:
			output.write(", "+model+"NestedSerializer")

	output.write("\n")

	output.write("from rest_framework.response import Response\n")
	output.write("from rest_framework.renderers import JSONRenderer\n")
	output.write("from rest_framework.decorators import api_view\n")
	output.write("from rest_framework.parsers import JSONParser\n")
	output.write("from rest_framework.decorators import permission_classes\n")
	output.write("from rest_framework import status\n")
	
	output.write("from django.http import HttpResponse, Http404, JsonResponse\n")
	output.write("from django.shortcuts import get_object_or_404\n")
	output.write("from django.forms.models import model_to_dict\n")
	output.write("from django.db.models import ProtectedError\n")
	
	output.write("import json\n")
	output.write("\n")

	output.write("class JSONResponse(HttpResponse):\n")
	output.write("\tdef __init__(self, data, **kwargs):\n")
	output.write("\t\tcontent = JSONRenderer().render(data)\n")
	output.write("\t\tkwargs['content_type'] = 'application/json'\n")
	output.write("\t\tsuper(JSONResponse, self).__init__(content, **kwargs)\n")
	output.write("\n")

	output.write("def get(request, modelName, serializerName = None, pk = None):\n")
	output.write("\tmodel = eval(modelName)\n")
	output.write("\tserializer = eval(serializerName)\n")
	output.write("\n")
	output.write("\tif pk is None:\n")
	output.write("\t\tmodel_object = model.objects.all()\n")
	output.write("\t\tserializer_object = serializer(model_object, many=True)\n")
	output.write("\telse :\n")
	output.write("\t\ttry:\n")
	output.write("\t\t\tmodel_object = model.objects.get(pk = pk)\n")
	output.write("\t\t\tserializer_object = serializer(model_object)\n")
	output.write("\t\texcept model.DoesNotExist:\n")
	output.write("\t\t\treturn Response(status = status.HTTP_404_NOT_FOUND)\n")
	output.write("\n")
	output.write("\treturn Response(serializer_object.data, status = status.HTTP_200_OK)\n")
	output.write("\n")

	output.write("def post(request, modelName, serializerName = None):\n")
	output.write("\tmodel = eval(modelName)\n")
	output.write("\tserializer = eval(serializerName)\n")
	output.write("\tserializer_object = serializer(data=request.data)\n")
	output.write("\n")
	output.write("\tif serializer_object.is_valid():\n")
	output.write("\t\tserializer_object.save()\n")
	output.write("\t\treturn Response(serializer_object.data, status=status.HTTP_201_CREATED)\n")
	output.write("\telse :\n")
	output.write("\t\treturn Response(serializer_object.errors, status = status.HTTP_400_BAD_REQUEST)\n")
	output.write("\n")
		
	output.write("def put(request, modelName, serializerName = None, pk = None):\n")
	output.write("\tmodel = eval(modelName)\n")
	output.write("\tserializer = eval(serializerName)\n")
	output.write("\n")
	output.write("\ttry:\n")
	output.write("\t\tmodel_object = model.objects.get(pk = pk)\n")
	output.write("\t\tserializer_object = serializer(model_object,data=request.data, partial=True)\n")
	output.write("\t\tif serializer_object.is_valid():\n")
	output.write("\t\t\tserializer_object.save()\n")
	output.write("\t\t\treturn Response(serializer_object.data, status=status.HTTP_200_OK)\n")
	output.write("\t\telse :\n")
	output.write("\t\t\treturn Response(serializer_object.errors, status = status.HTTP_400_BAD_REQUEST)\n")
	output.write("\texcept model.DoesNotExist:\n")
	output.write("\t\treturn Response(status = status.HTTP_404_NOT_FOUND)\n")
	output.write("\n")
	   

	output.write("def delete(request, modelName, pk = None):\n")
	output.write("\tif pk is None:\n")
	output.write("\t\treturn Response(status = status.HTTP_400_BAD_REQUEST)\n")
	output.write("\tmodel = eval(modelName)\n")
	output.write("\n")
	output.write("\ttry:\n")
	output.write("\t\tmodel_object = model.objects.get(pk = pk)\n")
	output.write("\t\tmodel_object.delete()\n")
	output.write("\texcept model.DoesNotExist:\n")
	output.write("\t\terror = \"The object you are looking for does not exist.\"\n")
	output.write("\t\treturn Response(error, status = status.HTTP_404_NOT_FOUND)\n")
	output.write("\texcept ProtectedError:\n")
	output.write("\t\terror = \"Cannot be deleted. This object is currently used.\"\n")
	output.write("\t\treturn Response(error, status = status.HTTP_400_BAD_REQUEST)\n")
	output.write("\treturn Response(status=status.HTTP_200_OK)\n")
	output.write("\n")


	for model in models:
		# check if it has a foreignkey
		fields = models[model]
		foreignKeyFields = []
		for field in fields:
			fieldObject = fields[field]
			if fieldObject.isForeignKey:
				foreignKeyFields.append(fieldObject)

		output.write("@api_view(['GET','POST','PUT','DELETE'])\n")
		output.write("def "+model+"API(request, pk = None):\n")
		output.write("\tmodelName=\""+model+"\"\n")
		output.write("\tserializerName=\""+model+"Serializer\"\n")
		output.write("\n")
		
		output.write("\tif request.method == 'GET':\n")
		output.write("\t\treturn get(request, modelName, serializerName, pk = pk)\n")
		output.write("\telif request.method == 'POST':\n")
		output.write("\t\treturn post(request, modelName, serializerName)\n")
		output.write("\telif request.method == 'PUT':\n")
		output.write("\t\treturn put(request, modelName, serializerName, pk = pk)\n")
		output.write("\telif request.method == 'DELETE':\n")
		output.write("\t\treturn delete(request, modelName, pk = pk)\n")
		output.write("\n")

		if foreignKeyFields:
			output.write("@api_view(['GET','POST','PUT','DELETE'])\n")
			output.write("def Nested"+model+"API(request, pk = None):\n")
			output.write("\tmodelName=\""+model+"\"\n")
			output.write("\tserializerName=\""+model+"NestedSerializer\"\n")
			output.write("\n")
			
			output.write("\tif request.method == 'GET':\n")
			output.write("\t\treturn get(request, modelName, serializerName, pk = pk)\n")
			output.write("\telif request.method == 'POST':\n")
			output.write("\t\treturn post(request, modelName, serializerName)\n")
			output.write("\telif request.method == 'PUT':\n")
			output.write("\t\treturn put(request, modelName, serializerName, pk = pk)\n")
			output.write("\telif request.method == 'DELETE':\n")
			output.write("\t\treturn delete(request, modelName, pk = pk)\n")
			output.write("\n")
	
