# Blog Application with Neurelo

This project is a blog application (CRUD) built with Neurelo.

## Overview

The majority of the code in this application is focused on managing various aspects, while the logic itself is concise thanks to Neurelo's capabilities.

## Features

1. **Retrieve User Information**
   - By user_id
   - By user_information (authentication required)
     - Includes functionality for signup and login in `authentication.py`

2. **Retrieve Posts**
   - All posts with related information (likes, comments, tags)

3. **Retrieve User's Posts**
   - Requires authentication
   - Option to add, delete, and edit posts for authorized users

4. **Likes and Comments**
   - Display likes and comments for each post

5. **Add and View Comments**
   - Users can add comments and view existing comments on posts

6. **Filter Posts**
   - Filter by time (Today, Last Week, Last Month)
   - Filter by tags (e.g., Technical, Machine Learning, Development, Neurelo)

