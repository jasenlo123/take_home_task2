from flask import Flask, request, jsonify
from datetime import datetime
from dashboard.models import User,UserSchema
from dashboard import app,db

# Init schema for User
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Get All User
@app.route('/user', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

# Get Single User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)