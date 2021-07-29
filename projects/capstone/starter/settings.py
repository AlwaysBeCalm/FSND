import os

from dotenv import load_dotenv
from models import *

load_dotenv()
database_path = "postgresql://{}:{}@{}/{}".format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST'),
    'library'
)


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def drop_all_create_all_add_record():
    # the next line will drop all the tables with their data every time the app starts/refreshes
    db.drop_all()
    db.create_all()

    # the next line is to add a single record in the database tables, and used for POSTMAN/UNIT_TEST testings
    add_record()


def add_record():
    author = Author()
    author.name = 'Abdullah'
    author.insert()

    category = Category()
    category.title = 'Programming'
    category.insert()

    book = Book(
        title='Java',
        pages=60,
        about='How to program in Java',
        author_id=1,
        category_id=1
    )
    book.insert()

    borrower = Borrower(name='Nasser')
    borrower.insert()

    borrowing_operation = BorrowedBooks(
        book_id=1,
        borrower_id=1
    )
    borrowing_operation.insert()
