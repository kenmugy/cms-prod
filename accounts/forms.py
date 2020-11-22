from django import forms
from django.contrib.auth.models import User
from .models import *

class OrderForm(forms.ModelForm):    	
	class Meta:
		model = Order
		fields = ['name','quantity']

class StoreOrderForm(forms.ModelForm):	
	class Meta:
		model = Order
		fields = ['status']

class OrderSearchForm(forms.ModelForm):
	name = forms.CharField(required=False)
	class Meta:
		model = Order
		fields = ["name", "status" ]

class ItemCreateForm(forms.ModelForm):    	
	class Meta:
		model = Item
		fields = ["item_no", "quantity"]
