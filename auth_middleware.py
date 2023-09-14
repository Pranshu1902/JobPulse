import jwt
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

def generateToken(id):
    token = jwt.encode({"user_id": id}, SECRET_KEY, algorithm="HS256")
    return token

def decodeToken(token):
    id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return id
