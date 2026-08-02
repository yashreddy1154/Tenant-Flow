from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.organizations.models import Organization

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Setup Org 1
        self.org1 = Organization.objects.create(name="Org 1")
        self.admin1 = User.objects.create_user(
            email="admin1@test.com", password="password", organization=self.org1, role="Admin"
        )
        self.member1 = User.objects.create_user(
            email="member1@test.com", password="password", organization=self.org1, role="Member"
        )
        
        # Setup Org 2
        self.org2 = Organization.objects.create(name="Org 2")
        self.admin2 = User.objects.create_user(
            email="admin2@test.com", password="password", organization=self.org2, role="Admin"
        )
        
    def test_team_management_data_isolation(self):
        self.client.login(email='admin1@test.com', password='password')
        response = self.client.get(reverse('team_management'))
        
        # Admin1 should see Member1 but not Admin2
        self.assertContains(response, 'member1@test.com')
        self.assertNotContains(response, 'admin2@test.com')
        
    def test_rbac_settings_access(self):
        # Admin can access
        self.client.login(email='admin1@test.com', password='password')
        response = self.client.get(reverse('org_settings'))
        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
        
        # Member cannot access
        self.client.login(email='member1@test.com', password='password')
        response = self.client.get(reverse('org_settings'))
        self.assertRedirects(response, reverse('home'))
        
    def test_rbac_billing_access(self):
        # Admin can access
        self.client.login(email='admin1@test.com', password='password')
        response = self.client.get(reverse('billing'))
        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
        
        # Member cannot access
        self.client.login(email='member1@test.com', password='password')
        response = self.client.get(reverse('billing'))
        self.assertRedirects(response, reverse('home'))
