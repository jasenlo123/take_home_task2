from datetime import datetime
from dashboard import db,ma
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}'')"
        
    def __init__(self, name, role, email, password):
      self.name = name
      self.role = role
      self.email = email
      self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(60), nullable=False)
    author_role = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def __init__(self, title, content, author_name,author_role):
      self.title = title
      self.content = content
      self.author_name = author_name
      self.author_role = author_role


# Product Schema
class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'date_posted', 'content', "author_name", "author_role")

# Product Schema
class UserSchema(ma.Schema):
  class Meta:
    posts = ma.Function(lambda obj: obj.category.category)
    fields = ('id', 'name', 'role', 'email', 'password')
