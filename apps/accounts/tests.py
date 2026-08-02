from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.organizations.models import Organization
from apps.accounts.forms import OrganizationSignupForm
from django.core import mail

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.invite_url = reverse('invite_member')
        
        # Setup Organization and Admin User
        self.org = Organization.objects.create(name="Test Org")
        self.admin_user = User.objects.create_user(
            email="admin@test.com", 
            password="password123",
            organization=self.org,
            role="Admin"
        )
        
        # Setup Member User
        self.member_user = User.objects.create_user(
            email="member@test.com", 
            password="password123",
            organization=self.org,
            role="Member"
        )

    def test_signup_creates_org_and_user(self):
        form_data = {
            'organization_name': 'New Org Inc',
            'industry_type': 'Tech',
            'company_size': 50,
            'email': 'newadmin@neworg.com',
            'password': 'StrongPassword1!'
        }
        response = self.client.post(self.signup_url, data=form_data)
        
        # Check redirection to home
        self.assertRedirects(response, reverse('home'))
        
        # Check org creation
        new_org = Organization.objects.filter(name='New Org Inc').first()
        self.assertIsNotNone(new_org)
        self.assertEqual(new_org.industry_type, 'Tech')
        self.assertEqual(new_org.company_size, 50)
        
        # Check user creation and role
        new_user = User.objects.filter(email='newadmin@neworg.com').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.organization, new_org)
        self.assertEqual(new_user.role, 'Admin')
        
    def test_login_flow(self):
        response = self.client.post(self.login_url, data={
            'username': 'admin@test.com',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))
        
    def test_invite_member_admin_only(self):
        # Login as Admin and invite
        self.client.login(email='admin@test.com', password='password123')
        response = self.client.post(self.invite_url, data={
            'email': 'newinvite@test.com',
            'role': 'Member',
            'department': 'Engineering'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(len(mail.outbox), 1)
        
        invited_user = User.objects.filter(email='newinvite@test.com').first()
        self.assertIsNotNone(invited_user)
        self.assertEqual(invited_user.organization, self.org)
        
        # Login as Member and try to invite
        self.client.logout()
        self.client.login(email='member@test.com', password='password123')
        response = self.client.post(self.invite_url, data={
            'email': 'anotherinvite@test.com',
            'role': 'Member'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(email='anotherinvite@test.com').exists())
