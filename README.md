# blog_application_with_neurelo
blog application (CRUD) with neurelo


## Most of the code is for managing things, logic is just one  liner with neurelo 

1. retrive user information by user_id ==> 

2. retrive user information by user_information ==> authentication.py -> signup, login

   users_api.find_users(filter=models.UsersWhereInput.from_dict({"email": email, "username": username}))
