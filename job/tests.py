from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company
from rest_framework import status
from rest_framework.test import APIClient
from .utils.tests.test_utils import TestUtils

class JobTest(TestCase, TestUtils):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="Test")
        self.company = self.create_company("Company1")
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

    def test_create_comment(self):
        job = self.create_job(applicant=self.user, role="SDE", company=self.company, platform="test", salary=100000, contract_length="Test", job_link="https://www.company.com")
        response = self.client.post(
            f'/jobs/{job.id}/comment/', {
                'comment': 'this is first comment',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
