from DB.db import connectDB

connect = connectDB()

cursor = connect.cursor()

def getUser(id):
    sql = '''
        SELECT * FROM user_db where id={}
        '''.format(id)
    
    cursor.execute(sql)
    result = cursor.fetchone()

    return result
