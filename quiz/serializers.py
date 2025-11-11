from rest_framework import serializers
from .models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'enonce', 'question_type', 'choices']

    
class QuizSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz 
        fields = ['id', 'title', 'questions', 'lesson']