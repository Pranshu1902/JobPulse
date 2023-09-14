from DB.db import connectDB

attributes = ['id', 'company', 'title', 'description', 'location', 'status', 'date_applied', 'url', 'platform', 'salary', 'contract_length', 'company_size']

connect = connectDB()
cursor = connect.cursor()

def generateJobResponseJSON(userID, jobID=''):
    sql = "SELECT "
    for i in range(len(attributes)):
        if i == len(attributes)-1:
            sql += attributes[i]
        else:
            sql += attributes[i] + ', '

    if len(jobID) == 0:
        sql += " FROM job where userid={};".format(userID)
    else:
        sql += " FROM job where userid={} AND id={};".format(userID, jobID)

    cursor.execute(sql)
    result = cursor.fetchall()

    data = []
    for job in result:
        jobJSON = {}
        for ind in range(len(attributes)):
            jobJSON[attributes[ind]] = job[ind]
        data.append(jobJSON)
    
    if len(jobID) != 0 and len(data) != 0:
        return data[0]
    return data

generateJobResponseJSON(1)
