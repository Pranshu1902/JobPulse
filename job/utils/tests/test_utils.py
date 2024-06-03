from job.models import *

class TestUtils:
    """Base class with basic methods to be used in tests"""

    @classmethod
    def create_company(self, name, **kwargs):
        data = {"name": name}
        data.update(kwargs)
        return Company.objects.create(**data)

    @classmethod
    def create_job(self, applicant, role, company, **kwargs):
        data = {"role": role, "company": company, "applicant": applicant}
        data.update(kwargs)
        return Job.objects.create(**data)
