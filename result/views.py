from models import Purchase_Order_Line
from serializers import Purchase_Order_LineSerializer, Purchase_Order_LineNestedSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import ProtectedError
import json

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def get(request, modelName, serializerName = None, pk = None):
	model = eval(modelName)
	serializer = eval(serializerName)

	if pk is None:
		model_object = model.objects.all()
		serializer_object = serializer(model_object, many=True)
	else :
		try:
			model_object = model.objects.get(pk = pk)
			serializer_object = serializer(model_object)
		except model.DoesNotExist:
			return Response(status = status.HTTP_404_NOT_FOUND)

	return Response(serializer_object.data, status = status.HTTP_200_OK)

def post(request, modelName, serializerName = None):
	model = eval(modelName)
	serializer = eval(serializerName)
	serializer_object = serializer(data=request.data)

	if serializer_object.is_valid():
		serializer_object.save()
		return Response(serializer_object.data, status=status.HTTP_201_CREATED)
	else :
		return Response(serializer_object.errors, status = status.HTTP_400_BAD_REQUEST)

def put(request, modelName, serializerName = None, pk = None):
	model = eval(modelName)
	serializer = eval(serializerName)

	try:
		model_object = model.objects.get(pk = pk)
		serializer_object = serializer(model_object,data=request.data, partial=True)
		if serializer_object.is_valid():
			serializer_object.save()
			return Response(serializer_object.data, status=status.HTTP_200_OK)
		else :
			return Response(serializer_object.errors, status = status.HTTP_400_BAD_REQUEST)
	except model.DoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)

def delete(request, modelName, pk = None):
	if pk is None:
		return Response(status = status.HTTP_400_BAD_REQUEST)
	model = eval(modelName)

	try:
		model_object = model.objects.get(pk = pk)
		model_object.delete()
	except model.DoesNotExist:
		error = "The object you are looking for does not exist."
		return Response(error, status = status.HTTP_404_NOT_FOUND)
	except ProtectedError:
		error = "Cannot be deleted. This object is currently used."
		return Response(error, status = status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_200_OK)

@api_view(['GET','POST','PUT','DELETE'])
def Purchase_Order_LineAPI(request, pk = None):
	modelName="Purchase_Order_Line"
	serializerName="Purchase_Order_LineSerializer"

	if request.method == 'GET':
		return get(request, modelName, serializerName, pk = pk)
	elif request.method == 'POST':
		return post(request, modelName, serializerName)
	elif request.method == 'PUT':
		return put(request, modelName, serializerName, pk = pk)
	elif request.method == 'DELETE':
		return delete(request, modelName, pk = pk)

@api_view(['GET','POST','PUT','DELETE'])
def NestedPurchase_Order_LineAPI(request, pk = None):
	modelName="Purchase_Order_Line"
	serializerName="Purchase_Order_LineNestedSerializer"

	if request.method == 'GET':
		return get(request, modelName, serializerName, pk = pk)
	elif request.method == 'POST':
		return post(request, modelName, serializerName)
	elif request.method == 'PUT':
		return put(request, modelName, serializerName, pk = pk)
	elif request.method == 'DELETE':
		return delete(request, modelName, pk = pk)

