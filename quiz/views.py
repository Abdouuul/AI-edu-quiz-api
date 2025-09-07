from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question

class QuizView(ViewSet):
    permission_classes = [IsAuthenticated]
    query_set = Quiz.objects.all()