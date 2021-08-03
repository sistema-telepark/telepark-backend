from abc import ABCMeta, abstractmethod
from typing import Type
from django.db import models
from django.http.response import JsonResponse
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from .static import http_method

class ICRUDStrategy(metaclass=ABCMeta):
    @abstractmethod
    def canHandle(self, method):
        pass

    @abstractmethod
    def handle(self, request, Model: Type[models.Model], ModelSerializer: Type[serializers.ModelSerializer]):
        pass

class PostStrategy(ICRUDStrategy):
    def canHandle(self, method):
        return method == http_method.POST

    def handle(self, request, Model: Type[models.Model], ModelSerializer: Type[serializers.ModelSerializer]):
        entity = JSONParser().parse(request)
        entitySerializer = ModelSerializer(data=entity)
        if entitySerializer.is_valid():
            entitySerializer.save()
            return JsonResponse(entitySerializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(entitySerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetStrategy(ICRUDStrategy):
    def canHandle(self, method):
        return method == http_method.GET

    def handle(self, request, Model: Type[models.Model], ModelSerializer: Type[serializers.ModelSerializer]):
        entities = Model.objects.all()
        return JsonResponse(ModelSerializer(entities, many=True).data, safe=False)

class OtherStrategy(ICRUDStrategy):
    def canHandle(self, method):
        return True

    def handle(self, request, Model: Type[models.Model], ModelSerializer: Type[serializers.ModelSerializer]):
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

class CRUDHandlerStrategies():
    strategies = [GetStrategy(), PostStrategy()]
    
    @staticmethod
    def getStrategy(method: str) -> ICRUDStrategy:
        return next((s for s in CRUDHandlerStrategies.strategies if s.canHandle(method)), OtherStrategy())