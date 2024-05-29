from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class JobTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="Test")
        self.company = Company.objects.create(name="Company1")
        self.user.set_password("12345678")
        self.user.save()

        response = self.client.post("/api-token-auth/", {"username": "Test", "password": "12345678"})
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)    

    def test_create_job(self):
        response = self.client.post(
            f'/jobs/', {
                'role': 'test',
                'platform': 'test',
                'salary': 100000,
                'contract_length': 'test',
                'company': self.company.id,
                "job_link": "https://www.company.com",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
