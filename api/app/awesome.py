# http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html
# Keeping this code for examples

import random
from flask import Flask, jsonify, request
from flasgger.utils import swag_from

from app import app

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from('awesome.yml')
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
