from django.test import TestCase
from django.contrib.auth.models import User
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
        self.force_login("Test", "12345678")

    def force_login(self, username, password):
        response = self.client.post(
            "/api-token-auth/", {"username": username, "password": password}
        )
        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_job(self):
        response = self.client.post(
            f"/jobs/",
            {
                "role": "test",
                "platform": "test",
                "salary": 100000,
                "contract_length": "test",
                "company": self.company.id,
                "job_link": "https://www.company.com",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment(self):
        job = self.create_job(
            applicant=self.user,
            role="SDE",
            company=self.company,
            platform="test",
            salary=100000,
            contract_length="Test",
            job_link="https://www.company.com",
        )
        response = self.client.post(
            f"/jobs/{job.id}/comment/",
            {
                "comment": "this is first comment",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_separate_user(self):
        job = self.create_job(
            applicant=self.user,
            role="SDE",
            company=self.company,
            platform="test",
            salary=100000,
            contract_length="Test",
            job_link="https://www.company.com",
        )

        # create new user
        user1 = User.objects.create(username="Test1")
        user1.set_password("12345678")
        user1.save()
        self.force_login("Test1", "12345678")

        # new user adding comment on job posting of other user
        response = self.client.post(
            f"/jobs/{job.id}/comment/",
            {
                "comment": "this is first comment",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action",
        )

    def test_update_status(self):
        job = self.create_job(
            applicant=self.user,
            role="SDE1",
            company=self.company,
            platform="test",
            salary=100000,
            contract_length="Test",
            job_link="https://www.company.com",
        )
        response = self.client.post(
            f"/jobs/{job.id}/update_status/",
            {
                "status": "Offered",
                "update_text": "Offer received",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_status_with_separate_user(self):
        job = self.create_job(
            applicant=self.user,
            role="SDE",
            company=self.company,
            platform="test",
            salary=100000,
            contract_length="Test",
            job_link="https://www.company.com",
        )

        # create new user
        user1 = User.objects.create(username="Test1")
        user1.set_password("12345678")
        user1.save()
        self.force_login("Test1", "12345678")

        # new user updating status on job posting of other user
        response = self.client.post(
            f"/jobs/{job.id}/update_status/",
            {
                "status": "Offered",
                "update_text": "Offer received",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action",
        )

    # def test_default_status_is_made_on_job_creation(self):
    #     job = self.create_job(applicant=self.user, role="SDE2", company=self.company, platform="test", salary=100000, contract_length="Test", job_link="https://www.company.com")
    #     response = self.client.get(
    #         f"/jobs/{job.id}/get_current_status/"
    #     )
    #     print(response.json())
    #     self.assertEqual(response.json()['status'], 'Applied')
