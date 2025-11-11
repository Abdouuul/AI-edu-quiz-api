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
    SINGLE_CHOICE = 'SC'
    MULTIPLE_CHOICE = 'MC'
    TRUE_FALSE = 'TF'
    OPEN_ENDED = 'OE'

    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True/False'),
        (OPEN_ENDED, 'Open Ended'),
    ]


    enonce = models.TextField()
    explication = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, null=True)
    choices = models.JSONField(default=list)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    open_question_answer = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.enonce