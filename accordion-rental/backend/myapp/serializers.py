from rest_framework import serializers
from .models import Model, Rendipillid

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'

class RendipillidSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.SerializerMethodField()
    mobile_image = serializers.SerializerMethodField()
    desktop_image = serializers.SerializerMethodField()
    
    modelId = ModelSerializer()  # Use modelId to match the field name in the Rendipillid model

    class Meta:
        model = Rendipillid
        fields = '__all__'
    
    def get_thumbnail_image(self, obj):
        return f"/media/300/R{obj.modelId.modelId}.jpg"
    
    def get_mobile_image(self, obj):
        return f"/media/700/R{obj.modelId.modelId}.jpg"

    def get_desktop_image(self, obj):
        return f"/media/1200/R{obj.modelId.modelId}.jpg"
