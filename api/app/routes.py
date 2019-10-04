# http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html

import random
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from

from app import app

Swagger(app)

@app.route("/")
def index():
    return """
        <h2>WHALECOM</h2>
        <a href="/hello">Row your boat</a>
    """

@app.route("/hello")
def hello():
    return """
        <h2>Whale, Hello World!</h2>
        <a href="/">Back to  whalecom</a><br />        
        <a href="/api/python/?size=5">Example</a><br /><br />
        <a href="/apidocs">Flasgger</a><br />Borrowed from <a href="http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html">Bruno Rocha</a>
    """

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from('example.yml')
def example(language):    
    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic", 
        "simple", "powerful", "amazing", 
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    notawesome = "An error occurred, invalid language for awesomeness"
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return notawesome, 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )

