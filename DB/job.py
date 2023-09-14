from db import connectDB

# connecting to the database
connect = connectDB()
cursor = connect.cursor()

def migrateJob():
    sql = '''
        CREATE TABLE job(
            id INT NOT NULL AUTO_INCREMENT,
            userid INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            company VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            role VARCHAR(20),
            status VARCHAR(20) NOT NULL,
            date_applied date NOT NULL,
            url VARCHAR(30),
            platform VARCHAR(20),
            salary INTEGER(7),
            contract_length INTEGER(3),
            company_size INTEGER(5),
            PRIMARY KEY (id),
            FOREIGN KEY (userid) REFERENCES user_db(id)
        )
    '''

    cursor.execute(sql)
    print("Job DB created")
    connect.close()
