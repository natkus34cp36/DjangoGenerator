import re, copy
from field import Field

def generateURL(models, appName):
	output = open("result/urls.py","w+")

	output.write("from django.conf.urls import url, include\n")
	output.write("from django.contrib import admin\n")
	output.write("from "+appName+" import views\n")
	output.write("from rest_framework.urlpatterns import format_suffix_patterns\n")
	output.write("\n")
	
	output.write("urlpatterns = [\n")
	for model in models:
		output.write("\turl(r'^"+model.lower()+"/$', views."+model+"API, name='"+model.lower()+"'),\n")
		output.write("\turl(r'^"+model.lower()+"/(?P<pk>[0-9]+)$', views."+model+"API, name='"+model.lower()+"-detail'),\n")
	output.write("]\n\n")

	output.write("urlpatterns += [\n")
	output.write("\turl(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),\n")
	output.write("]\n")
	output.write("urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])\n")
