from sms_app.config import config_env_files
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import tomllib

db = SQLAlchemy()

def prepare_app(p_db=db):
    app = Flask(__name__)
    app.config.from_object(config_env_files["new"])
    p_db.init_app(app)
    with open("config.toml", "rb") as f:
        confi = tomllib.load(f)
    return app

app = prepare_app()
#migrate = Migrate(app, db)

from . import views

def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit
