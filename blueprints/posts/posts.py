from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for 
from neurelo import models 

from configuration import posts_api 

posts = Blueprint('posts', __name__, template_folder='templates', url_prefix='/posts')

@posts.route('/get_posts/<user_id>')
def get_posts_by_user_id(user_id):
    select = models.PostsSelectInput.from_dict({"$scalars": True, "$related": True})
    filter = models.PostsWhereInput.from_dict({"user_id": {"equals": int(user_id)}})
    filter.__fields_set__.remove('content')
    response = posts_api.find_posts(select, filter)
    return jsonify(response.to_dict()) 
