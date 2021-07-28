import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
database_path = "postgresql://{}:{}@{}/{}".format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST'),
    'library'
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.create_all()
