'''
1) Right click the table from Microsoft SQL Workbench, Select "Copy SQL to Clipboard"
2) Copy to a text file
3) Delete the first line and replace every ` to an empty string (not space)
4) Name it <Model> without any extension
5) Change "CHANGE_HERE" to <Model> in getModelFromFile("CHANGE_HERE") statement
6) Run the program

*** README ***
1) This program does not scan for foreign_key, thus the foreign_key field will be INT type
2) The max_length of CharField will always be 45 (I'm lazy to get size)
'''

from ReadFileToModels import getFieldsFromFile
from ModelGenerator import generateModel
from SerializersGenerator import generateSerializer
from ViewGenerator import generateView
from UrlGenerator import generateURL
from AdminGenerator import generateAdmin
from EasyGenerator import generateEasy
from field import Field

fileName = "xxx"
appName = "sale"
models = getFieldsFromFile(fileName)
generateModel(models)
generateSerializer(models, appName)
generateView(models)
generateURL(models, appName)
generateAdmin(models, appName)
generateEasy(models)
