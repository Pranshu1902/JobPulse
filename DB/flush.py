from db import connectDB

connect = connectDB()

cursor = connect.cursor()

tables = ['job', 'user_db']

for table in tables:
    sql = '''
        DROP TABLE IF EXISTS {}
    '''.format(table)
    cursor.execute(sql)

connect.commit()
connect.close()
