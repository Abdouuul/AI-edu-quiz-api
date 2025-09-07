from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Lesson

class LessonView(ViewSet):
    permission_classes = [IsAuthenticated]
    query_set = Lesson.objects.all()


    def post(self, request):
        #
        #
        #
        # Code to generate the lesson 

        return Response({"message": "Lesson Created!"})