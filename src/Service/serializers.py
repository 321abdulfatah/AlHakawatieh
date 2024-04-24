# import serializer from rest_framework
from rest_framework import serializers
from django.core.validators import RegexValidator

# import model from models.py
from .models import Client,Service



# Create a model serializer

class clientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Client
		fields = ('__all__')

class ServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Service
		fields = ('__all__')
