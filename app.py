from flask import Flask, Blueprint
from api.user import userRoutes
from api.job import jobRoutes
from api.jobUpdate import jobUpdateRoutes

app = Flask(__name__)

api = Blueprint('api', __name__, url_prefix='/api/v1/')

# user routes
api.register_blueprint(userRoutes)

# job routes
api.register_blueprint(jobRoutes)

# job update routes
api.register_blueprint(jobUpdateRoutes)

# register the api
app.register_blueprint(api)


# run the app
app.run(debug=True)
