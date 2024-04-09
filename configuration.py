import os
from dotenv import load_dotenv 

from neurelo.configuration import Configuration 
from neurelo.api_client import ApiClient 
from neurelo.api.posts_api import PostsApi
from neurelo.api.users_api import UsersApi 
from neurelo.api.comments_api import CommentsApi
from neurelo.models import (UsersCreateInput,UsersSelectInput, UsersUpdateInput,
                            PostsCreateInput, PostsSelectInput, PostsUpdateInput, 
                            CommentsCreateInput, CommentsSelectInput, CommentsUpdateInput)

load_dotenv() 

NEURELO_API_HOST = os.getenv("NEURELO_API_HOST") or ""
NEURELO_API_KEY = os.getenv("NEURELO_API_KEY") or ""

if not NEURELO_API_HOST:
    raise ValueError("NEURELO_API_HOST environment variable is not set")
if not NEURELO_API_KEY:
    raise ValueError("NEURELO_API_KEY environment variable is not set")


configuration = Configuration(host=NEURELO_API_HOST, api_key={'ApiKey': NEURELO_API_KEY})
api_client = ApiClient(configuration=configuration) 
users_api = UsersApi(api_client)
posts_api = PostsApi(api_client)
comments_api = CommentsApi(api_client)