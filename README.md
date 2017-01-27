# DjangoGenerator
## This project was initiated to reduce workload when the database designer (SQL) and requirements had to work hard innovating the best design. This plug-and-play generator was to test and deploy APIs with Django-Rest-Framework. The format was written by using the developers' style to make it ready for further modification.

## Requirements:
* Python 2 and Django set up.
* SQL CREATE Command from MySQLWorkBench.

## What will it generate.
admin.py -> Enable Django-Rest-Framework APIs UI.
models.py -> Models generated in Django Class and Fields according the design from MySQLWorkBench.
serializers.py -> Nested and non-nested serializers for all tables generated.
urls.py -> A standard routing CRUD path for this application.
views.py -> CRUD Function-based views for all tables generated.
easy.txt -> Listed all the fields in every table (This one was created to reduce typo and typing time).

# Steps:
1. Create a "result" folder next to this file.
2. Select table(s) from the design in MySQLWorkBench and copy SQL Command.
3. Create a file named "xxx" and place it next to this file.
4. Replace "'" with an empty string.
5. Open the generator.py and change appName value to your application name, run generator.py.
6. Copy the files in result folder to your Django application. Don't forget to install and route your new application!
