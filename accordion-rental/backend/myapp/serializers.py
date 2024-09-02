from rest_framework import serializers
from .models import Model, Rendipillid

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class RendipillidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rendipillid
        fields = '__all__'
