from flask import Flask, request, jsonify
from datetime import datetime
from dashboard.models import Post,PostSchema
from dashboard import app,db
from flask_login import (
    current_user
)

# Init schema for Post
post_schema = PostSchema()
posts_schema = PostSchema(many=True)



# CREATE a Post
@app.route('/post', methods=['POST'])
def add_post():
  title = request.json["title"]
  content = request.json["content"]

  new_post = Post(title = title, content = content, author_name = current_user.name, author_role = current_user.role )
  
  db.session.add(new_post)
  db.session.commit()

  return post_schema.jsonify(new_post)

# Get All Posts
@app.route('/post', methods=['GET'])
def get_posts():
  all_posts = Post.query.all()
  result = posts_schema.dump(all_posts)
  return jsonify(result)


# Delete post
@app.route('/post', methods=['DELETE'])
def delete_post():

  id = request.json["id"]
  post = Post.query.get(id)
  db.session.delete(post)
  db.session.commit()

  return post_schema.jsonify(post)

# Delete post
@app.route('/post', methods=['PUT'])
def update_post():

  id = request.json["id"]
  title = request.json["title"]
  content = request.json["content"]

  post = Post.query.get_or_404(id)
  post.title = title
  post.content = content
  db.session.commit()

  return post_schema.jsonify(post)
  
  