from flask import Flask, request, jsonify
from datetime import datetime
from dashboard.models import User,UserSchema
from dashboard import app,db, bcrypt
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import generate_csrf

#login manager init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


# Init schema for User
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Get All User
@app.route('/user', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)


def get_user(id: int):
    user = User.query.filter_by(id=id).first()
    if int(id) == int(id):
        return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user
    return None


#login route
@app.route("/user/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
      login_user(user)
      return jsonify({"login": True})

    else:
      return jsonify({"login": False})


@app.route("/user/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response



@app.route("/user/getsession", methods=["GET"])
def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})
    return jsonify({"login": False})

#get name
@app.route("/user/data", methods=["GET"])
@login_required
def user_data():
    user = get_user(current_user.id)
    return jsonify({"name": user.name})

#logout
@app.route("/user/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"logout": True})