from flask import request, jsonify, Blueprint
from DB.db import connectDB
from auth_middleware import generateToken


userRoutes = Blueprint('userRoutes', __name__, template_folder='templates')


connect = connectDB()
cursor = connect.cursor()
# sign up route
@userRoutes.route('/user/signup', methods=['POST'])
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
@userRoutes.route('/user/login', methods=['POST'])
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
