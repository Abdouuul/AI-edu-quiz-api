from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Lesson
from rest_framework_simplejwt.tokens import RefreshToken


class LessonAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.lesson_data = {'title': 'Test Lesson', 'content': 'This is a test lesson content.'}
        self.lesson = Lesson.objects.create(title='Existing Lesson', content='Content of existing lesson')

    def test_create_lesson(self):
        url = reverse('lesson-list') 
        response = self.client.post(url, self.lesson_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.get(title='Test Lesson').content, 'This is a test lesson content.')

    def test_get_lessons(self):
        url = reverse('lesson-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_lesson(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        updated_data = {'title': 'Updated Lesson', 'content': 'Updated content.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')
        self.assertEqual(self.lesson.content, 'Updated content.')

    def test_delete_lesson(self):
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)