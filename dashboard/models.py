from datetime import datetime
from dashboard import db,ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
        
    def __init__(self, name, role, email, password,posts):
      self.name = name
      self.role = role
      self.email = email
      self.password = password
      self.posts = posts

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# Product Schema
class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'date_posted', 'content', "user_id")

# Product Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'role', 'email', 'password','posts')
