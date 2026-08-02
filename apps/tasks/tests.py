import json
from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.organizations.models import Organization
from apps.projects.models import Project
from apps.tasks.models import Task, TaskComment, Subtask
from apps.notifications.models import Notification

class TaskTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.org = Organization.objects.create(name="Org")
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", organization=self.org, role="Admin"
        )
        self.member = User.objects.create_user(
            email="member@test.com", password="password", organization=self.org, role="Member"
        )
        self.project = Project.objects.create(
            name="Project",
            organization=self.org,
            team_leader=self.admin
        )
        self.task = Task.objects.create(
            title="Task 1",
            project=self.project,
            status="Todo",
            priority="High",
            assignee=self.member
        )

    def test_task_status_api(self):
        self.client.login(email='member@test.com', password='password')
        url = reverse('task_update_status_api', args=[self.task.pk])
        
        # Test Drag & Drop API
        response = self.client.post(url, data=json.dumps({'status': 'Done'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'Done')

    def test_task_assignment_notification(self):
        self.client.login(email='admin@test.com', password='password')
        
        # Clear existing notifications created by signals/views if any
        Notification.objects.all().delete()
        
        response = self.client.post(reverse('task_create'), data={
            'title': 'New Task',
            'project': self.project.pk,
            'status': 'Todo',
            'priority': 'High',
            'assignee': self.member.pk
        })
        
        # Verify notification was created
        notif = Notification.objects.filter(recipient=self.member).first()
        self.assertIsNotNone(notif)
        self.assertIn('assigned', notif.message.lower())

    def test_subtask_and_comment_creation(self):
        self.client.login(email='member@test.com', password='password')
        
        # Test Subtask creation
        self.client.post(reverse('task_subtask_create', args=[self.task.pk]), data={
            'title': 'Subtask 1'
        })
        self.assertTrue(Subtask.objects.filter(task=self.task, title='Subtask 1').exists())
        
        # Test Comment creation
        self.client.post(reverse('task_comment_create', args=[self.task.pk]), data={
            'text': 'This is a comment.'
        })
        self.assertTrue(TaskComment.objects.filter(task=self.task, text='This is a comment.').exists())
