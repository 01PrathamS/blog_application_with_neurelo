from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for 
from neurelo import models 

from configuration import posts_api 

posts = Blueprint('posts', __name__, template_folder='templates', url_prefix='/posts')

@posts.route('/get_posts/<user_id>')
def get_posts_by_user_id(user_id):
    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    filter = models.PostsWhereInput.from_dict({"user_id": {"equals": int(user_id)}})
    filter.__fields_set__.remove('content')
    posts = posts_api.find_posts(select, filter)
    # return jsonify(response.to_dict()) 
    return render_template('my_posts.html', posts=posts.to_dict()['data'])

@posts.route('/add_post/<user_id>', methods=['POST', 'GET']) 
def add_post_by_user_id(user_id): 
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if session['user_id']:
            post_input = models.PostsCreateInput(title=title, content=content, posts_users_ref={"connect":{"user_id":int(user_id)}}) 
            posts_api.create_one_posts(post_input) 
            return redirect(url_for('posts.get_posts_by_user_id', user_id=session['user_id']))
        else: 
            return redirect(url_for('authentication.login'))
    return render_template('add_post.html')

@posts.route('edit_post/<post_id>', methods=['POST', 'GET'])
def edit_post_by_post_id(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content'] 
        if session['user_id']: 
            post_input = models.PostsUpdateInput.from_dict({"title":title, "content":content})
            posts_api.update_posts_by_post_id(str(post_id), post_input)
            return redirect(url_for('posts.get_posts_by_user_id', user_id=session['user_id']))
        else: 
            return redirect(url_for('authentication.login')) 
    else: 
        post = posts_api.find_posts_by_post_id((post_id), select=models.PostsSelectInput(title=True, content=True))
        return render_template('edit_post.html', post=post.to_dict()['data'], post_id=post_id)
 

