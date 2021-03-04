from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'de26a2ccabac416b0cc068d4051cee04'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

from dashboard import post_routes,user_routes