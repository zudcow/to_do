import unittest
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Task


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, task_description='Test Task', date_added=timezone.now(), completed=False)

    def test_task_creation(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.task_description, 'Test Task')
        self.assertEqual(task.completed, False)

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(user=self.user, task_description='Test Task', date_added=timezone.now(), completed=False)

    def test_index_view(self):
        response = self.client.get(reverse('to_do:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'to_do/index.html')

    def test_complete_task_view(self):
        response = self.client.post(reverse('to_do:complete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 204)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.completed, True)

    def test_delete_task_view(self):
        response = self.client.post(reverse('to_do:delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertEqual(Task.objects.filter(id=self.task.id).exists(), False)

    def test_add_task_view(self):
        response = self.client.post(reverse('to_do:add_task'), {'new_task': 'New Task'})
        self.assertEqual(response.status_code, 302)  # Redirects after adding a task
        self.assertEqual(Task.objects.filter(task_description='New Task').exists(), True)

    def test_add_subtask_view(self):
        response = self.client.post(reverse('to_do:add_subtask', args=[self.task.id]), {'subtask_{}'.format(self.task.id): 'Subtask'})
        self.assertEqual(response.status_code, 302)  # Redirects after adding a subtask
        subtask = Task.objects.filter(task_description='Subtask', parent_task=self.task)
        self.assertEqual(subtask.exists(), True)

    def test_completed_tasks_view(self):
        response = self.client.get(reverse('to_do:completed_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'to_do/completed.html')
