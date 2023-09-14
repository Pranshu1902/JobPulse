import mysql.connector

def connectDB():
    connect = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='jobpulse')
    return connect
