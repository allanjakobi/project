from rest_framework import generics
from .models import Model, Rendipillid
from .serializers import ModelSerializer, RendipillidSerializer

class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class RendipillidList(generics.ListCreateAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer

