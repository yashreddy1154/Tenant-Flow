import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.models import User
from apps.organizations.models import Organization
from apps.documents.models import Document

class DocumentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.org = Organization.objects.create(name="Org")
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password", organization=self.org, role="Admin"
        )
        self.member = User.objects.create_user(
            email="member@test.com", password="password", organization=self.org, role="Member"
        )
        
    def test_document_upload(self):
        self.client.login(email='member@test.com', password='password')
        
        # Create a dummy file
        dummy_file = SimpleUploadedFile("test_file.txt", b"file content")
        
        response = self.client.post(reverse('document_upload'), data={
            'name': 'Test Document',
            'file': dummy_file
        })
        
        self.assertRedirects(response, reverse('document_list'))
        
        doc = Document.objects.filter(name='Test Document').first()
        self.assertIsNotNone(doc)
        self.assertEqual(doc.organization, self.org)
        self.assertEqual(doc.uploaded_by, self.member)
        
    def test_document_deletion_permissions(self):
        # Member 1 uploads a doc
        doc = Document.objects.create(
            name="Member Doc",
            file="dummy.txt",
            organization=self.org,
            uploaded_by=self.member
        )
        
        # Admin can delete it
        self.client.login(email='admin@test.com', password='password')
        response = self.client.post(reverse('document_delete', args=[doc.pk]))
        self.assertRedirects(response, reverse('document_list'))
        self.assertFalse(Document.objects.filter(pk=doc.pk).exists())
