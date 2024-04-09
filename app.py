from flask import Flask, redirect, url_for, request, jsonify, session, render_template

from neurelo import models
from configuration import users_api
from configuration import posts_api

import secrets
secret_key = secrets.token_hex(16)

app = Flask(__name__) 
app.secret_key = secret_key

@app.route('/')
def index(): 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=24644)