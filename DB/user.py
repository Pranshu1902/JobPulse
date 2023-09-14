#import mysql.connector
from db import connectDB

# connecting to the database
#connect = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='jobpulse')
connect = connectDB()

# running the queries
cursor = connect.cursor()

def migrateUser():
   cursor.execute("DROP TABLE IF EXISTS user_db")

   #Creating user table
   sql = '''
      CREATE TABLE user_db(
         id INT NOT NULL AUTO_INCREMENT,
         name CHAR(20) NOT NULL,
         email varchar(40) NOT NULL,
         password varchar(40) NOT NULL,
         PRIMARY KEY (id)
      )'''

   cursor.execute(sql)
   print("User DB created")
   connect.close()
