from flask import Flask, redirect, url_for, request, jsonify, session, render_template

from neurelo import models
from configuration import users_api, posts_api
from blueprints.authentication import authentication
from blueprints.posts import posts
from blueprints.comments import comments

import secrets
secret_key = secrets.token_hex(16)

app = Flask(__name__) 
app.register_blueprint(authentication.authentication)
app.register_blueprint(posts.posts)
app.register_blueprint(comments.comments)
app.secret_key = secret_key

@app.route('/')
def index(): 
    ## check if the user is already login --> if user_id already stored in session storage 
    if 'user_id' in session: 
        from blueprints.posts import posts
        posts = posts.get_all_posts()
        return render_template('index.html', posts=posts) 
    else: 
        return redirect(url_for('authentication.login'))
    

if __name__ == '__main__':
    app.run(debug=True, port=24644)