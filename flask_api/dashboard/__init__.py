from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt



app = Flask(__name__,static_folder="public")
app.config['SECRET_KEY'] = 'de26a2ccabac416b0cc068d4051cee04'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'

app.config.update(
    DEBUG=True,
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

csrf = CSRFProtect(app)
cors = CORS(
    app,
    resources={r"*": {"origins": "http://localhost:8080"}},
    expose_headers=["Content-Type", "X-CSRFToken"],
    supports_credentials=True,
)

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
# Init hash check
bcrypt = Bcrypt(app)


from dashboard import post_routes,user_routes