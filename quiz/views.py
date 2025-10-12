from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Quiz, Question
from .serializers import QuizSerializer
from rest_framework.response import Response
from ai_generator.graph import quiz_generator_graph, GeneratorState


class QuizView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        lesson_id = request.data.get("lesson_id")

        print("lesson id : ", lesson_id)
        user = request.user
        if user.is_anonymous:
                    return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not lesson_id:
            return Response({"error": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        initial_state = GeneratorState(
              user_id= user.id,
              lesson_id=lesson_id
        )
        result = quiz_generator_graph.invoke(initial_state)
        
        return Response({
            "reply": result['reply'],
            "questions": [q.dict() for q in result['questions']]
        })