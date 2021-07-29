from flask_script import Manager
from flask_migrate import Migrate

from app import app
from models import db

migrate = Migrate(app, db)
manager = Manager(app)


if __name__ == '__main__':
    manager.run()