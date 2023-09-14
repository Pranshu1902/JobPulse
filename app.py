from flask import Flask, request, Response, jsonify
from DB.db import connectDB
import os
from auth_middleware import generateToken, decodeToken
from job_middleware import generateJobResponseJSON

app = Flask(__name__)
connect = connectDB()
cursor = connect.cursor()

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
app.config['SECRET_KEY'] = SECRET_KEY

# sign up route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.args

    # check for same email
    check_email_sql = '''
        SELECT * FROM user_db where email='{}';
    '''.format(data['email'])
    cursor.execute(check_email_sql)
    result = cursor.fetchone()

    if result:
        return jsonify({'response': 'Email already exists'})

    sql = '''
        INSERT INTO user_db(name, email, password) values('{}', '{}', '{}');
    '''.format(data['name'], data['email'], data['password'])

    cursor.execute(sql)
    connect.commit()

    return jsonify(
        {'id': cursor.rowcount, 'message': 'success'}
    )
    # return 'Signed up with id={}'.format(cursor.rowcount)

# login route
@app.route('/login', methods=['POST'])
def login():
    data = request.args

    sql = '''
        SELECT * FROM user_db WHERE email='{}' AND password='{}';
    '''.format(data['email'], data['password'])

    cursor.execute(sql)
    result = cursor.fetchone()

    if result is None:
        return jsonify({'response': 'Invalid Credentials'})
    else:
        id = result[0]
        # JWT
        token = generateToken(id)
        return jsonify({'id': id, 'message': 'Logged in successfully', 'token': token})

@app.route('/job/create', methods=['POST'])
def createJob():
    data = request.args
    token = request.headers['Token']

    # authorize user
    try:
        user = decodeToken(token)
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})

    sql = '''
        INSERT INTO job(title, description, userid, location, status, company, date_applied) values('{}', '{}', '{}', '{}', '{}', '{}', '{}');
    '''.format(data['title'], data['description'], user['user_id'], data['location'], data['status'], data['company'], data['date_applied'])

    cursor.execute(sql)
    connect.commit()

    # all job body attributes
    response = {
        'id': cursor.rowcount,
        'company': data['company'],
        'title': data['title'],
        'description': data['description'],
        'location': data['location'],
        'status': data['status'],
        'userid': user['user_id'],
        'date_applied': data['date_applied'],
        'url': data['url'],
        'platform': data['platform'],
        'salary': data['salary'],
        'contract_length': data['contract_length'],
        'company_size': data['company_size'],
    }

    return jsonify({'message': 'Job created successfully', 'response': response})

@app.route('/job', methods=['GET'])
def getJobs():
    try:
        user = decodeToken(request.headers['Token'])
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    data = generateJobResponseJSON(user['user_id'])

    return jsonify({'data': data, 'message': 'success'})

@app.route('/job/<id>', methods=['GET'])
def getSpecificJob(id):
    try:
        user = decodeToken(request.headers['Token'])
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    data = generateJobResponseJSON(user['user_id'], id)

    return jsonify({'data': data, 'message': 'success'})

@app.route('/job/<id>', methods=['PUT'])
def updateJob(id):
    try:
        user = decodeToken(request.headers['Token'])
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    # check if user has access
    data = generateJobResponseJSON(user['user_id'], id)
    if len(data) != 0:
        attr = []
        for i in request.args.items():
            attr.append(i[0])
        
        sql = "UPDATE job SET "
        for i in range(len(attr)):
            if i == len(attr)-1:
                if request.args[attr[i]].isalpha():
                    sql += attr[i] + "='{}'".format(request.args[attr[i]])
                else:
                    sql += attr[i] + '=' + request.args[attr[i]]
            else:
                if request.args[attr[i]].isalpha():
                    sql += attr[i] + "='{}', ".format(request.args[attr[i]])
                else:
                    sql += attr[i] + '=' + request.args[attr[i]] + ', '
        sql += ' WHERE id={};'.format(id)

        print(sql)

        cursor.execute(sql)
        connect.commit()

        updatedData = generateJobResponseJSON(user['user_id'], id)

        return jsonify({'message': 'success', 'response': updatedData})
    return jsonify({'message': 'Invalid Job ID'})

@app.route('/job/<id>', methods=['DELETE'])
def deleteJob(id):
    try:
        user = decodeToken(request.headers['Token'])
    except Exception as e:
        return jsonify({'response': 'Invalid Token'})
    
    # check if user has access
    data = generateJobResponseJSON(user['user_id'], id)
    if len(data) != 0:
        sql = '''
            DELETE FROM job where id={}
        '''.format(id)
        cursor.execute(sql)
        connect.commit()

        return jsonify({'message': 'success', 'response': 'Job deleted'})
    return jsonify({'message': 'Invalid Job ID'})


app.run(debug=True)
