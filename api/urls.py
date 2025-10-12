from rest_framework import routers
from lesson.views import LessonView
from quiz.views import QuizView

router = routers.DefaultRouter()

router.register(r'lessons', LessonView, basename='lesson')
router.register(r'quizs', QuizView, basename='quiz')