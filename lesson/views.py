from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Lesson
from .serializers import LessonSerializer

class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def post(self, request):
        #
        #
        #
        # Code to save a lesson

        return Response({"message": "Lesson Created!"})