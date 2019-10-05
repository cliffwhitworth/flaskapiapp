from flask import Flask, jsonify, request

from app import app

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
        <a href="/restful">Restful Example</a><br />         
        <a href="/api/python/?size=5">Example</a><br /><br />
        <a href="/apidocs">Flasgger</a><br />Borrowed from <a href="http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html">Bruno Rocha</a>
    """