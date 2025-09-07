from django.db import models
from lesson.models import Lesson

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quizzes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Question(models.Model):
    enonce = models.TextField()
    explication = models.TextField(blank=True, null=True)
    choices = models.JSONField(default=list)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.enonce