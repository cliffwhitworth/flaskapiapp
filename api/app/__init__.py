from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

from app.users import usersAPI
from app.auth import authenticate
from app import routes
from app import hello
from app import awesome

# Uncomment for local testing without docker-compose
# app.run(debug=True, host='0.0.0.0')
