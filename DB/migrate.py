from user import migrateUser
from job import migrateJob
from DB.jobUpdate import migrateJobUpdate

migrateUser()
migrateJob()
migrateJobUpdate()
