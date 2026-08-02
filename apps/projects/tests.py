from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.organizations.models import Organization
from apps.projects.models import Project

class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Setup Org 1
        self.org1 = Organization.objects.create(name="Org 1")
        self.admin1 = User.objects.create_user(
            email="admin1@test.com", password="password", organization=self.org1, role="Admin"
        )
        self.manager1 = User.objects.create_user(
            email="manager1@test.com", password="password", organization=self.org1, role="Manager"
        )
        self.project1 = Project.objects.create(
            name="Alpha Project",
            organization=self.org1,
            team_leader=self.manager1
        )
        
        # Setup Org 2
        self.org2 = Organization.objects.create(name="Org 2")
        self.admin2 = User.objects.create_user(
            email="admin2@test.com", password="password", organization=self.org2, role="Admin"
        )
        self.project2 = Project.objects.create(
            name="Beta Project",
            organization=self.org2,
            team_leader=self.admin2
        )

    def test_project_isolation(self):
        self.client.login(email='admin1@test.com', password='password')
        response = self.client.get(reverse('project_list'))
        
        self.assertContains(response, 'Alpha Project')
        self.assertNotContains(response, 'Beta Project')
        
    def test_project_creation_admin_only(self):
        self.client.login(email='manager1@test.com', password='password')
        response = self.client.get(reverse('project_create'))
        self.assertRedirects(response, reverse('project_list'))
        
        self.client.logout()
        self.client.login(email='admin1@test.com', password='password')
        response = self.client.post(reverse('project_create'), data={
            'name': 'New Project',
            'status': 'Active',
            'team_leader': self.manager1.pk
        })
        self.assertRedirects(response, reverse('project_list'))
        self.assertTrue(Project.objects.filter(name='New Project').exists())
        
    def test_project_edit_manager(self):
        self.client.login(email='manager1@test.com', password='password')
        response = self.client.post(reverse('project_edit', args=[self.project1.pk]), data={
            'name': 'Alpha Project Updated',
            'status': 'Archived',
            'team_leader': self.manager1.pk
        })
        self.assertRedirects(response, reverse('project_detail', args=[self.project1.pk]))
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Alpha Project Updated')
        self.assertEqual(self.project1.status, 'Archived')
