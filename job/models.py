import uuid
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("Applied", "Applied"),
    ("Rejected", "Rejected"),
    ("Offered", "Offered"),
    ("Accepted", "Accepted"),
    ("Withdrawn", "Withdrawn"),
)

# PLATFORM_CHOICES = (
#     ("LinkedIn", "LinkedIn"),
#     ("Glassdoor", "Glassdoor"),
#     ("Indeed", "Indeed"),
#     ("Unstop", "Unstop"),
# )

# COMPANY_SIZE_CHOICES = (
#     ("1-10", "1-10"),
#     ("11-50", "11-50"),
#     ("51-200", "51-200"),
#     ("201-1000", "201-1000"),
#     ("1000>", "1000>"),
# )


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=False, blank=False)
    # founded = models.IntegerField()
    # website = models.URLField()
    # size = models.CharField(max_length=15, choices=COMPANY_SIZE_CHOICES)

    def __str__(self) -> str:
        return f"{self.name}"


# TODO: decide and probably remove the Company model class altogether else update the Job's perform_create method
# to automatically create a Company object for each Job


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=30, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # company = models.CharField(max_length=40, null=False, blank=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=30, null=False, blank=False)
    # status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Applied")
    application_date = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField()
    contract_length = models.CharField(max_length=15)
    job_link = models.URLField()

    def __str__(self):
        print(f"{self.role}- {self.company}- {self.status}")

    # Create a JobUpdate object automatically when the Job is created
    # Also, create a new company automatically with basic details to be added by the user later


class JobStatusUpdate(models.Model):
    """Model to keep track of all updates made to the job status"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="statuses")
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="Applied",
        null=False,
        blank=False,
    )
    update_text = models.CharField(max_length=100, default="Initialize Job")
    date_posted = models.DateField(auto_now_add=True)


# show in timeline view


class JobComment(models.Model):
    """Model to store the comments added for each job application"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(auto_now_add=True)
