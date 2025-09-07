from rest_framework import serializers
from .models import Quiz, Question

class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz 
        fields = ['enonce']