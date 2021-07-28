import unittest

from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, os


class LibraryTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

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
            # self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_for_endpoint(self):

        # test the end point when getting 'get' method
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

        # test the end point when getting 'post' method
        res = self.client().post('/')
        self.assertEqual(res.status_code, 405)

    def test_get_all_authors(self):

        # test getting all authors with an author token
        manager_token = os.environ.get('manager_token', None)
        # test getting all authors with the token of an author
        headers = {'Authorization': 'Bearer {}'.format(manager_token)}
        res = self.client().get('/authors/', headers=headers)
        self.assertEqual(res.status_code, 200)

        # test getting all author without the token of an author
        res = self.client().get('/authors/')
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
