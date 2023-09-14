from db import connectDB

# connecting to the database
connect = connectDB()
cursor = connect.cursor()

def migrateJobUpdate():
    sql = '''
        CREATE TABLE job_update(
            id INT NOT NULL AUTO_INCREMENT,
            jobid INT NOT NULL,
            message VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (jobid) REFERENCES job(id)
        )
    '''

    cursor.execute(sql)
    print("Job Update DB created")
    connect.close()
