import website
from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
#frontend = website.create_app()
#waitressserve(frontend, host="0.0.0.0", port=80)
app = Flask(__name__)
app.config["SECRET_KEY"] = "LOLTHISISNOTSECURE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
from website.models import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# register blueprints
from website.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)
from website.content import content as content_blueprint
app.register_blueprint(content_blueprint)