from flask import Blueprint, jsonify, request, render_template,flash, session, redirect, url_for 
from neurelo import models 

from configuration import posts_api, likes_api

posts = Blueprint('posts', __name__, template_folder='templates', url_prefix='/posts')

# @posts.route('/get_posts')
def get_all_posts():
    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    posts = posts_api.find_posts(select)
    return posts.to_dict()['data']

@posts.route('/get_posts/<user_id>')
def get_posts_by_user_id(user_id):
    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    filter = models.PostsWhereInput.from_dict({"user_id": {"equals": int(user_id)}})
    filter.__fields_set__.remove('content')
    posts = posts_api.find_posts(select, filter)
    ## count likes for user's all the posts
    likes = 0 
    for post in posts.to_dict()['data']:
        if post['posts_likes_ref']:
            likes += len(post['posts_likes_ref'])
    print(likes)
    # return jsonify(response.to_dict()) 
    return render_template('my_posts.html', posts=posts.to_dict()['data'], likes=likes)

@posts.route('/add_post/<user_id>', methods=['POST', 'GET']) 
def add_post_by_user_id(user_id): 
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if session['user_id']:
            post_input = models.PostsCreateInput(title=title,
                                                 content=content, 
                                                 posts_users_ref={"connect":{"user_id":int(user_id)}},
                                                 post_tags_ref={"connect": {"tag_id": 1}}) 
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
 
@posts.route('delete_post/<post_id>', methods=['POST', 'GET']) 
def delete_post_by_post_id(post_id):
    if session['user_id']:
        posts_api.delete_posts_by_post_id(post_id) 
        return redirect(url_for('posts.get_posts_by_user_id', user_id=session['user_id']))
    else: 
        return redirect(url_for('authentication.login')) 
    

@posts.route('view_post/<post_id>', methods=['GET'])
def get_post_by_post_id(post_id):
    post = posts_api.find_posts_by_post_id((post_id), select=models.PostsSelectInput(related=True, scalars=True))
    return render_template('view_post.html', post=post.to_dict()['data'])

@posts.route('/create_like/<int:post_id>', methods=['GET'])
def create_like_by_post_id(post_id):
    if 'user_id' not in session:
        return redirect(url_for('authentication.login'))
    user_id = session['user_id']
    response = likes_api.create_one_likes(models.LikesCreateInput(
        like=True,
        likes_posts_ref={"connect": {"post_id": post_id}},
        likes_users_ref={"connect": {"user_id": user_id}}
    ))
    print(response.to_dict())
    return redirect(url_for('index'))

@posts.route('/filter_post/<tag_id>', methods=['GET'])
def filter_post_by_tag_id(tag_id):
    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    filter = models.PostsWhereInput.from_dict({"tag_id": {"equals": int(tag_id) }}) 
    filter.__fields_set__.remove('content')  
    posts = posts_api.find_posts(select, filter)
    return render_template('index.html', posts=posts.to_dict()['data'])

## we are filtering posts by time, by today, this week, this month.and this is sample code 
@posts.route('/filter_post_by_time/<time>', methods=['GET'])
def filter_post_by_time(time):
    from datetime import datetime, timedelta
    now = datetime.now()
    if time == 'today':
        start_date = now.date()
        time_filter = start_date.isoformat() + 'T00:00:00Z'
        filter = models.PostsWhereInput.from_dict({"posted_at": {"gte": time_filter}})
    elif time == 'week':
        start_date = (now - timedelta(days=now.weekday())).date()
        time_filter = start_date.isoformat() + 'T00:00:00Z'
        filter = models.PostsWhereInput.from_dict({"posted_at": {"gte": time_filter}})
    elif time == 'month':
        start_date = now.replace(day=1).date()
        time_filter = start_date.isoformat() + 'T00:00:00Z'
        filter = models.PostsWhereInput.from_dict({"posted_at": {"gte": time_filter}})
    else: 
       return jsonify({"error": "Invalid time filter specified"}), 400

    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    order_by = [models.PostsOrderByWithRelationInput.from_dict({"post_id": "desc"})]
    filter.__fields_set__.remove('content')
    posts = posts_api.find_posts(select, filter, order_by)
    return render_template('index.html', posts=posts.to_dict()['data'])

