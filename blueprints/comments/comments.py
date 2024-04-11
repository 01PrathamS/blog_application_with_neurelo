from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from neurelo import models
from configuration import comments_api

comments = Blueprint('comments', __name__, template_folder='templates', url_prefix='/comments')

@comments.route('/view_comment/<post_id>')
def get_comments_by_post_id(post_id):
    # select = models.CommentsSelectInput(select=True,related=True)
    filter = models.CommentsWhereInput.from_dict({"post_id": int(post_id)})
    comments = comments_api.find_comments(filter=filter)
    return render_template('view_comments.html', comments=comments.to_dict()['data'], id=post_id)

@comments.route('/add_comment/<post_id>', methods=['POST', 'GET'])
def add_comment_by_post_id(post_id): 
    if request.method == "GET":
        comment = request.form['comment']
        user_id = session['user_id']
        comment_input = models.CommentsCreateInput(comment=comment,
                                            comments_posts_ref={"connect":{"post_id":int(post_id)}},
                                            comments_users_ref={"connect":{"user_id":int(user_id)}})
        comments_api.create_one_comments(comment_input)
        return redirect(url_for('index'))
    else: 
        print("**********")
        print(type(post_id))
        print("**********")
        return render_template('view_comments.html', id=post_id)