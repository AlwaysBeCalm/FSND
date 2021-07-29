import unittest

from flask_sqlalchemy import SQLAlchemy

from app import app
from settings import setup_db, os


class LibraryManagerTestCase(unittest.TestCase):
    """This class represents the test cases of the manager of the library application"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            "library")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_for_root_endpoint(self):
        # test the end point when getting 'get' method
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

        # test the end point when getting 'post' method
        res = self.client().post('/')
        self.assertEqual(res.status_code, 405)

    def test_get_all_authors_by_manager(self):
        # test getting all authors with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting all authors with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all authors without the token of manager
        res = self.client().get('/authors/')
        self.assertEqual(res.status_code, 401)

    def test_get_an_author_by_manager(self):
        # test getting an author with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting an author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting an author without the token of manager
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist author with the token of manager (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_an_author_by_manager(self):
        # test adding an author with manager token
        manager_token = os.environ.get('manager_token', None)
        new_author = {
            'name': 'Test 1'
        }

        # test adding an author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().post('/authors/', json=new_author, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_an_author_by_manager(self):
        # test updating an author with manager token
        manager_token = os.environ.get('manager_token', None)
        new_author = {
            'name': 'Updated Author name'
        }

        # test updating an author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/authors/1/update', json=new_author, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating an author without the token of manager
        res = self.client().patch('/authors/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_an_author_by_manager(self):
        # test delete an author with manager token
        manager_token = os.environ.get('manager_token', None)

        # test deleting an author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().delete('/authors/2/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test delete an author without the token of manager
        res = self.client().delete('/authors/2/delete')
        self.assertEqual(res.status_code, 401)

    def test_getting_an_author_books_by_manager(self):
        # test getting an author books with manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting an author books with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/1/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting an author books without the token of manager
        res = self.client().get('/authors/1/books')
        self.assertEqual(res.status_code, 401)

    def test_get_all_categories_by_manager(self):
        # test getting all categories with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting all categories with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/categories/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all categories without the token of an author
        res = self.client().get('/categories/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_category_by_manager(self):
        # test getting a category with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a category with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/categories/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist category with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/categories/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a category without the token of manager
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist category with the token of manager (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/categories/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_a_category_by_manager(self):
        # test adding a category with manager token
        manager_token = os.environ.get('manager_token', None)
        new_category = {
            'title': 'New Category'
        }

        # test adding a category with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().post('/categories/', json=new_category, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_category_by_manager(self):
        # test updating a category with manager token
        manager_token = os.environ.get('manager_token', None)
        new_category = {
            'title': 'Updated Category title'
        }

        # test updating a category with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/categories/1/update', json=new_category, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a category without the token of manager
        res = self.client().patch('/categories/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_a_category_by_manager(self):
        # test delete a category with manager token
        manager_token = os.environ.get('manager_token', None)

        # test deleting a category with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().delete('/categories/2/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test deleting a category without the token of manager
        res = self.client().delete('/categories/2/delete')
        self.assertEqual(res.status_code, 401)

    def test_getting_a_category_books_by_manager(self):
        # test getting a category books with manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a category books with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/categories/1/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a category books without the token of manager
        res = self.client().get('/categories/1/books')
        self.assertEqual(res.status_code, 401)

    def test_get_all_books_by_manager(self):
        # test getting all books with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting all books with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all books without the token of manager
        res = self.client().get('/books/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_book_by_manager(self):
        # test getting a book with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/books/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/books/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a book without the token of manager
        res = self.client().get('/books/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist book with the token of manager (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/books/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_a_book_by_manager(self):
        # test adding a book with manager token
        manager_token = os.environ.get('manager_token', None)
        new_book = {
            'title': 'New Book',
            'pages': 100,
            'about': 'Test adding a new Book',
            'author_id': 1,
            'category_id': 1,
        }

        # test adding a book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().post('/books/', json=new_book, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_book_by_manager(self):
        # test updating a book with manager token
        manager_token = os.environ.get('manager_token', None)
        new_book = {
            'title': 'Updated Book title',
            'about': 'Test updating book title',
            'author_id': 1,
            'category_id': 1,
        }

        # test updating a book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/books/1/update', json=new_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a book without the token of manager
        res = self.client().patch('/books/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_a_book_by_manager(self):
        # test delete a book with manager token
        manager_token = os.environ.get('manager_token', None)

        # test deleting a book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().delete('/books/1/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test deleting a book without the token of manager
        res = self.client().delete('/books/1/delete')
        self.assertEqual(res.status_code, 401)

    def test_getting_a_book_borrowers_by_manager(self):
        # test getting a book borrowers with manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a book borrowers with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/books/2/borrowers/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a book borrowers without the token of manager
        res = self.client().get('/books/2/borrowers')
        self.assertEqual(res.status_code, 401)

    def test_get_all_borrowers_by_manager(self):
        # test getting all borrowers with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting all borrowers with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowers/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all borrowers without the token of an author
        res = self.client().get('/borrowers/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_borrower_by_manager(self):
        # test getting a borrower with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowers/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowers/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a borrower without the token of manager
        res = self.client().get('/borrowers/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist borrowers with the token of manager (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowers/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_a_borrower_by_manager(self):
        # test adding a borrower with manager token
        manager_token = os.environ.get('manager_token', None)
        new_borrower = {
            'name': 'New Borrower',
        }

        # test adding a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().post('/borrowers/', json=new_borrower, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_borrower_by_manager(self):
        # test updating a borrower with manager token
        manager_token = os.environ.get('manager_token', None)
        new_borrower = {
            'name': 'Updated borrower name'
        }

        # test updating a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowers/1/update', json=new_borrower, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a borrower without the token of manager
        res = self.client().patch('/borrowers/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_a_borrower_by_manager(self):
        # test delete a borrower with manager token
        manager_token = os.environ.get('manager_token', None)

        # test deleting a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().delete('/borrowers/2/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test deleting a borrower without the token of manager
        res = self.client().delete('/borrowers/2/delete')
        self.assertEqual(res.status_code, 401)

    def test_getting_a_borrower_books_by_manager(self):
        # test getting a borrower books with manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a borrower books with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowers/2/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a borrower books without the token of manager
        res = self.client().get('/borrowers/2/books')
        self.assertEqual(res.status_code, 401)

    def test_get_all_borrowed_books_by_manager(self):
        # test getting all borrowed books with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting all borrowed books with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowed_books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all borrowed books without the token of an author
        res = self.client().get('/borrowed_books/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_borrowed_book_by_manager(self):
        # test getting a borrowed book with a manager token
        manager_token = os.environ.get('manager_token', None)

        # test getting a borrowed book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowed_books/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist borrowed book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowed_books/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a borrowed book without the token of manager
        res = self.client().get('/borrowed_books/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist borrowed book with the token of manager (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/borrowed_books/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_a_borrowed_book_by_manager(self):
        # test adding a borrowed book with manager token
        manager_token = os.environ.get('manager_token', None)
        new_borrowed_book = {
            'book_id': 1,
            'borrower_id': 1,
        }

        # test adding a borrowed book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().post('/borrowed_books/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_borrowed_book_by_manager(self):
        # test updating a borrowed book with manager token
        manager_token = os.environ.get('manager_token', None)
        new_borrowed_book = {
            'book_id': 1,
            'borrower_id': 1,
        }

        # test updating a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowed_books/1/update', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a borrowed book with manager token and give it wrong book id
        new_borrowed_book = {
            'book_id': 1000,
            'borrower_id': 1,
        }

        # test updating a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowed_books/1/update', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 400)

        # test updating a borrowed book with manager token and give it wrong category id
        new_borrowed_book = {
            'book_id': 1,
            'borrower_id': 1000,
        }

        # test updating a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowed_books/1/update', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 400)

        # test updating a borrower without the token of manager
        res = self.client().patch('/borrowed_books/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_a_borrowed_book_by_manager(self):
        # test delete a borrowed book with manager token
        manager_token = os.environ.get('manager_token', None)

        # test deleting a borrowed book with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().delete('/borrowed_books/2/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test deleting a borrower without the token of manager
        res = self.client().delete('/borrowed_books/2/delete')
        self.assertEqual(res.status_code, 401)

    def test_return_a_borrowed_book_by_manager(self):
        # test updating a borrowed book with manager token
        manager_token = os.environ.get('manager_token', None)
        new_borrowed_book = {
            'rating': 3.5
        }

        # test returning a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowed_books/1/return/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test returning a borrowed book with manager token and give it wrong rating
        new_borrowed_book = {
            'rating': 99.65
        }

        # test updating a borrower with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().patch('/borrowed_books/1/return', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 400)

        # test updating a borrower without the token of manager
        res = self.client().patch('/borrowed_books/1/return')
        self.assertEqual(res.status_code, 401)


class LibraryAuthorTestCase(unittest.TestCase):
    """This class represents the test cases of the author of the library application"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            "library")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_for_root_endpoint(self):
        # test the end point when getting 'get' method
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

        # test the end point when getting 'post' method
        res = self.client().post('/')
        self.assertEqual(res.status_code, 405)

    def test_get_all_authors_by_author(self):
        # test getting all authors with a author token
        author_token = os.environ.get('author_token', None)

        # test getting all authors with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/authors/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all authors without the token of author
        res = self.client().get('/authors/')
        self.assertEqual(res.status_code, 401)

    def test_get_an_author_by_author(self):
        # test getting an author with a author token
        author_token = os.environ.get('author_token', None)

        # test getting an author with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/authors/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist author with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/authors/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting an author without the token of author
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist author with the token of author (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/authors/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    # this to get the current author's books
    def test_getting_an_author_books_by_author(self):
        # test getting an author books with author token
        author_token = os.environ.get('author_token', None)

        # test getting an author books with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/authors/1/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting an author books without the token of author
        res = self.client().get('/authors/1/books')
        self.assertEqual(res.status_code, 401)

    def test_update_an_author_by_author(self):
        # test updating an author with author token
        author_token = os.environ.get('author_token', None)
        new_author = {
            'name': 'Updated Author name'
        }

        # test updating an author with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().patch('/authors/1/update', json=new_author, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating an author without the token of author
        res = self.client().patch('/authors/1/update')
        self.assertEqual(res.status_code, 401)

    def test_get_all_books_by_author(self):
        # test getting all books with a author token
        author_token = os.environ.get('author_token', None)

        # test getting all books with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all books without the token of author
        res = self.client().get('/books/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_book_by_author(self):
        # test getting a book with a author token
        author_token = os.environ.get('author_token', None)

        # test getting a book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/books/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/books/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a book without the token of author
        res = self.client().get('/books/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist book with the token of author (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/books/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_add_a_book_by_author(self):
        # test adding a book with author token
        author_token = os.environ.get('author_token', None)
        new_book = {
            'title': 'New Book',
            'pages': 100,
            'about': 'Test adding a new Book',
            'author_id': 1,
            'category_id': 1,
        }

        # test adding a book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().post('/books/', json=new_book, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_book_by_author(self):
        # test updating a book with author token
        author_token = os.environ.get('author_token', None)
        new_book = {
            'title': 'Updated Book title',
            'about': 'Test updating book title',
            'author_id': 1,
            'category_id': 1,
        }

        # test updating a book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().patch('/books/1/update', json=new_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a book without the token of author
        res = self.client().patch('/books/1/update')
        self.assertEqual(res.status_code, 401)

    def test_delete_a_book_by_author(self):
        # test delete a book with author token
        author_token = os.environ.get('author_token', None)

        # test deleting a book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().delete('/books/1/delete/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test deleting a book without the token of author
        res = self.client().delete('/books/1/delete')
        self.assertEqual(res.status_code, 401)

    # this to get the names of the borrowers of the current author's books
    def test_getting_a_book_borrowers_by_author(self):
        # test getting a book borrowers with author token
        author_token = os.environ.get('author_token', None)

        # test getting a book borrowers with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/books/2/borrowers/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a book borrowers without the token of author
        res = self.client().get('/books/2/borrowers')
        self.assertEqual(res.status_code, 401)

    def test_get_all_categories_by_author(self):
        # test getting all categories with a author token
        author_token = os.environ.get('author_token', None)

        # test getting all categories with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/categories/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all categories without the token of an author
        res = self.client().get('/categories/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_category_by_author(self):
        # test getting a category with a author token
        author_token = os.environ.get('author_token', None)

        # test getting a category with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/categories/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist category with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/categories/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a category without the token of author
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist category with the token of author (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/categories/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_borrower_by_author(self):
        # test updating a borrower with author token
        author_token = os.environ.get('author_token', None)
        new_borrower = {
            'name': 'Updated borrower name'
        }

        # test updating a borrower with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().patch('/borrowers/1/update', json=new_borrower, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a borrower without the token of author
        res = self.client().patch('/borrowers/1/update')
        self.assertEqual(res.status_code, 401)

    def test_getting_a_borrower_books_by_author(self):
        # test getting a borrower books with author token
        author_token = os.environ.get('author_token', None)

        # test getting a borrower books with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().get('/borrowers/2/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a borrower books without the token of author
        res = self.client().get('/borrowers/2/books')
        self.assertEqual(res.status_code, 401)

    def test_add_a_borrowed_book_by_author(self):
        # test adding a borrowed book with author token
        author_token = os.environ.get('author_token', None)
        new_borrowed_book = {
            'book_id': 1,
            'borrower_id': 1,
        }

        # test adding a borrowed book with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().post('/borrowed_books/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_return_a_borrowed_book_by_author(self):
        # test updating a borrowed book with author token
        author_token = os.environ.get('author_token', None)
        new_borrowed_book = {
            'rating': 3.5
        }

        # test returning a borrower with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().patch('/borrowed_books/1/return/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test returning a borrowed book with author token and give it wrong rating
        new_borrowed_book = {
            'rating': 99.65
        }

        # test updating a borrower with the token of author
        headers = {'Authorization': 'Bearer {}'.format(author_token)}
        res = self.client().patch('/borrowed_books/1/return', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 400)

        # test updating a borrower without the token of author
        res = self.client().patch('/borrowed_books/1/return')
        self.assertEqual(res.status_code, 401)


class LibraryBorrowerTestCase(unittest.TestCase):
    """This class represents the test cases of the borrower (user) of the library application"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            "library")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_for_root_endpoint(self):
        # test the end point when getting 'get' method
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

        # test the end point when getting 'post' method
        res = self.client().post('/')
        self.assertEqual(res.status_code, 405)

    def test_get_all_authors_by_borrower(self):
        # test getting all authors with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting all authors with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/authors/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all authors without the token of borrower
        res = self.client().get('/authors/')
        self.assertEqual(res.status_code, 401)

    def test_get_an_author_by_borrower(self):
        # test getting an author with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting an author with the token of manager
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/authors/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist author with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/authors/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting an author without the token of borrower
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist author with the token of borrower (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/authors/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_getting_an_author_books_by_borrower(self):
        # test getting an author books with borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting an author books with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/authors/1/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting an author books without the token of borrower
        res = self.client().get('/authors/1/books')
        self.assertEqual(res.status_code, 401)

    def test_get_all_categories_by_borrower(self):
        # test getting all categories with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting all categories with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/categories/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all categories without the token of an borrower
        res = self.client().get('/categories/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_category_by_borrower(self):
        # test getting a category with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting a category with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/categories/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist category with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/categories/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a category without the token of borrower
        res = self.client().get('/authors/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist category with the token of borrower (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/categories/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_getting_a_category_books_by_borrower(self):
        # test getting a category books with borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting a category books with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/categories/1/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a category books without the token of borrower
        res = self.client().get('/categories/1/books')
        self.assertEqual(res.status_code, 401)

    def test_get_all_books_by_borrower(self):
        # test getting all books with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting all books with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/books/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all books without the token of a borrower
        res = self.client().get('/books/')
        self.assertEqual(res.status_code, 401)

    def test_get_a_book_by_borrower(self):
        # test getting a book with a borrower token
        borrower_token = os.environ.get('borrower_token', None)

        # test getting a book with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/books/1', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting a non-exist book with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/books/1000', headers=headers)
        self.assertEqual(res.status_code, 404)

        # test getting a book without the token of borrower
        res = self.client().get('/books/1')
        self.assertEqual(res.status_code, 401)

        # test getting a non-exist book with the token of borrower (fail-case)
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().get('/books/10000', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_borrower_by_borrower(self):
        # test updating a borrower with borrower token
        borrower_token = os.environ.get('borrower_token', None)
        new_borrower = {
            'name': 'Updated borrower name'
        }

        # test updating a borrower with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().patch('/borrowers/1/update', json=new_borrower, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test updating a borrower without the token of borrower
        res = self.client().patch('/borrowers/1/update')
        self.assertEqual(res.status_code, 401)

    def test_add_a_borrowed_book_by_borrower(self):
        # test adding a borrowed book borrower borrower token
        borrower_token = os.environ.get('borrower_token', None)
        new_borrowed_book = {
            'book_id': 1,
            'borrower_id': 1,
        }

        # test adding a borrowed book with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().post('/borrowed_books/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_return_a_borrowed_book_by_manager(self):
        # test updating a borrowed book with borrower token
        borrower_token = os.environ.get('borrower_token', None)
        new_borrowed_book = {
            'rating': 3.5
        }

        # test returning a borrower with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().patch('/borrowed_books/1/return/', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 200)

        # test returning a borrowed book with borrower token and give it wrong rating
        new_borrowed_book = {
            'rating': 99.65
        }

        # test updating a borrower with the token of borrower
        headers = {'Authorization': 'Bearer {}'.format(borrower_token)}
        res = self.client().patch('/borrowed_books/1/return', json=new_borrowed_book, headers=headers)
        self.assertEqual(res.status_code, 400)

        # test updating a borrower without the token of borrower
        res = self.client().patch('/borrowed_books/1/return')
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
