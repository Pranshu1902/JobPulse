from flask import request, jsonify, Blueprint
from DB.db import connectDB
from auth_middleware import generateToken, decodeToken


jobUpdateRoutes = Blueprint('jobUpdateRoutes', __name__)


connect = connectDB()
cursor = connect.cursor()

# create job update
@jobUpdateRoutes.route('/job/<jobid>/update/create', methods=['POST'])
def createJobUpdate(jobid):
    data = request.args
    token = request.headers['Token']

    # authorize user
    try:
        user = decodeToken(token)
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    sql = '''
        INSERT INTO job_update(jobid, message, date) values('{}', '{}', '{}');
    '''.format(jobid, data['message'], data['date'])

    cursor.execute(sql)
    connect.commit()

    return jsonify({'response': 'success', 'jobid': jobid, 'message': data['message'], 'date': data['date']})

# get job update route
@jobUpdateRoutes.route('/job/<jobid>/update', methods=['GET'])
def getJibUpdates(jobid):
    data = request.args
    token = request.headers['Token']

    # authorize user
    try:
        user = decodeToken(token)
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})

    sql = '''
        SELECT * FROM job_update WHERE jobid='{}';
    '''.format(jobid)

    cursor.execute(sql)
    result = cursor.fetchall()

    # generate json
    json = []
    for row in result:
        json.append({
            'id': row[0],
            'jobid': row[1],
            'message': row[2],
            'date': row[3]
        })

    if result is None:
        return jsonify({'response': 'Invalid Credentials'})
    else:
        return jsonify({'message': 'success', 'response': json})

# delete job update route
@jobUpdateRoutes.route('/job/<jobid>/update/<updateid>/delete', methods=['DELETE'])
def delJobUpdate(jobid, updateid):
    data = request.args
    token = request.headers['Token']

    # authorize user
    try:
        user = decodeToken(token)
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})

    sql = '''
        DELETE FROM job_update WHERE jobid='{}' AND id='{}';
    '''.format(jobid, updateid)

    cursor.execute(sql)
    connect.commit()

    return jsonify({'response': 'success', 'jobid': jobid, 'updateid': updateid})

# update job update route
@jobUpdateRoutes.route('/job/<jobid>/update/<updateid>/update', methods=['PUT'])
def updJobUpdate(jobid, updateid):
    data = request.args
    token = request.headers['Token']

    # authorize user
    try:
        user = decodeToken(token)
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    attr = []
    for i in request.args.items():
        attr.append(i[0])
    
    sql = "UPDATE job_update SET message='{}' WHERE id={};".format(data['message'], updateid)

    cursor.execute(sql)
    connect.commit()

    return jsonify({'message': 'success', 'id': updateid, 'jobid': jobid, 'message': data['message']})
