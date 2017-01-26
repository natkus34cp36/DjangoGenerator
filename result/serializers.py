from rest_framework import serializers
from sale.models import Purchase_Order_Line

class Purchase_Order_LineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Purchase_Order_Line

class Purchase_Order_LineNestedSerializer(serializers.ModelSerializer):

	class Meta:
		model = Purchase_Order_Line
		depth = 1

