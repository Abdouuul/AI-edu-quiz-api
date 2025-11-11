from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from lesson.models import Lesson
from .models import Quiz, Question
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

class QuizAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.lesson = Lesson.objects.create(title='Test Lesson', content='This is a test lesson content.')
        self.quiz_data = {
            'title': 'Test Quiz',
            'lesson': self.lesson.id,
        }
        self.quiz = Quiz.objects.create(title='Existing Quiz', lesson=self.lesson)
        Question.objects.create(
            quiz=self.quiz,
            enonce='What is the capital of France?',
            question_type='SC',
            choices={'Paris': True, 'London': False}
        )

    def test_create_quiz(self):
        url = reverse('quiz-list')
        response = self.client.post(url, self.quiz_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)
        self.assertEqual(Quiz.objects.get(title='Test Quiz').lesson, self.lesson)

    def test_get_quizzes(self):
        url = reverse('quiz-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.quiz.title)

    def test_get_single_quiz(self):
        url = reverse('quiz-detail', kwargs={'pk': self.quiz.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.quiz.title)
        self.assertEqual(len(response.data['questions']), 1)