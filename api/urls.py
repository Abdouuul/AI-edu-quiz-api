from rest_framework import routers
from lesson.views import LessonView

router = routers.DefaultRouter()

router.register(r'lessons', LessonView, basename='lesson')
