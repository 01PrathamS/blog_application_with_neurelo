from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for 
from neurelo import models 

from configuration import users_api 

authentication = Blueprint('authentication', __name__, template_folder='templates', url_prefix='/authentication')

@authentication.route('/login', methods=['POST', 'GET'])
def login(): 
    if request.method == 'POST': 
        username = request.form['username'] 
        email = request.form['email'] 
        ## to check if the user present in the database 
        user = users_api.find_users(filter=models.UsersWhereInput.from_dict({"email": email, 
                                                                             "username": username}))
        if (user.to_dict())["data"]: ## if the user is there store user_data in session_storage 
            user_data = user.to_dict()['data'][0]
            session['user_id'] = user_data['user_id'] 
            session['username'] = user_data['username'] 
            session['email'] = user_data['email']
            return redirect(url_for('posts.get_posts_by_user_id',user_id=session['user_id']))
        else: ## if there is no match found return with message
            return render_template("login.html", message="User does not exist") 
    else: 
        if session.get('user_id', None): 
            return f"you are ok {session['username']}"
        return render_template("login.html", message="Welcome!!")
    
@authentication.route('/signup', methods=['POST', 'GET'])
def signup(): 
    if request.method == 'POST': 
        username = request.form['username']
        email = request.form['email']
        ## first let's check if the user already exists or not.
        user = users_api.find_users(filter=models.UsersWhereInput.from_dict({"email": email, 
                                                                             "username": username}))
        if (user.to_dict())["data"]:
            return render_template("signup.html", message="User already exists")
        else: 
            user_input = models.UsersCreateInput(username=username, email=email)
            users_api.create_one_users(user_input)
            return redirect(url_for('authentication.login'))
    else: 
        return render_template("signup.html")
    

@authentication.route('/logout') 
def logout(): 
    session.clear()
    return redirect(url_for('authentication.login'))