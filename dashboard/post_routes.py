from flask import Flask, request, jsonify
from datetime import datetime
from dashboard.models import Post,PostSchema
from dashboard import app,db

# Init schema for Post
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


# Test
@app.route('/', methods=['GET'])
def test():
  return jsonify({'msg':'helloworld'})

# CREATE a Post
@app.route('/post', methods=['POST'])
def add_post():
  title = request.json['title']
  content = request.json['content']

  new_post = Post(title = title, content = content)

  db.session.add(new_post)
  db.session.commit()

  return post_schema.jsonify(new_post)

# Get All Posts
@app.route('/post', methods=['GET'])
def get_posts():
  all_posts = Post.query.all()
  result = posts_schema.dump(all_posts)
  return jsonify(result)

# Get Single Post
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
  post = Post.query.get(id)
  return post_schema.jsonify(post)

# Update a post
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
  post = Post.query.get(id)

  title = request.json['title']
  content = request.json['content']

  post.title = title
  post.content = content

  db.session.commit()

  return post_schema.jsonify(post)

# Delete post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
  post = Post.query.get(id)
  db.session.delete(post)
  db.session.commit()

  return post_schema.jsonify(post)