from django.conf.urls import url, include
from django.contrib import admin
from sale import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^purchase_order_line/$', views.Purchase_Order_LineAPI, name='purchase_order_line'),
	url(r'^purchase_order_line/(?P<pk>[0-9]+)$', views.Purchase_Order_LineAPI, name='purchase_order_line-detail'),
]

urlpatterns += [
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
