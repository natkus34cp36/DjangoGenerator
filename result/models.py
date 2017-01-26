from __future__ import unicode_literals
from django.db import models
from datetime import date

class Purchase_Order_Line(models.Model):
	PurchaseOrderLine_id = models.AutoField(primary_key=True, null=False)
	PurchaseOrder_id = models.ForeignKey("Purchase_Order", on_delete=models.PROTECT, db_column = 'PurchaseOrder_id', null=False)
	Product_id = models.ForeignKey("Product", on_delete=models.PROTECT, db_column = 'Product_id', null=False)
	FOBUnitPrice = models.FloatField(default=0)
	CIFUnitPrice = models.FloatField(default=0, null=True)
	Quantity = models.IntegerField(default=0)
	TotalNetWeight = models.FloatField(default=0)
	TotalShippingWeight = models.FloatField(default=0)
	TotalPrice = models.FloatField(default=0)
	EstSalePrice = models.FloatField(default=0)
	EstSaleTotal = models.FloatField(default=0)

	class Meta:
		db_table = 'Purchase_Order_Line'

