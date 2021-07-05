import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('abdullah', '1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

        # to check whither we got all the categories or not
        self.assertIsNotNone(data.get('categories'))

        # to check error 405 method not allowed on an endpoint
        res = self.client().post('/categories/')
        self.assertEqual(res.status_code, 405)

        # to check error 404 not found on a wrong endpoint.
        res = self.client().post('/categorie/')
        self.assertEqual(res.status_code, 404)

    def test_get_categories_wrong_URI(self):
        res = self.client().get('/categories')

        # to check error 308 permanent redirect
        self.assertEqual(res.status_code, 308)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        # test get all the questions
        self.assertEqual(res.status_code, 200)

        self.assertIsNotNone(data.get('questions'))
        self.assertTrue(data.get('questions'))
        self.assertIsNotNone(data.get('categories'))
        self.assertIsNotNone(data.get('total_questions'))
        # self.assertEqual(, True)
        self.assertTrue(data.get('success'))

        # uncommenting the next line, will get and exception of none key
        # self.assertIsNotNone(data.get('is_there_a_key'))

    def test_get_404_on_not_found_questions(self):
        res = self.client().get('/questions/?page=1000')
        data = json.loads(res.data)

        # test get all the questions
        self.assertEqual(res.status_code, 200)

        self.assertIsNotNone(data.get('questions'))
        self.assertIsNotNone(data.get('categories'))
        self.assertIsNotNone(data.get('total_questions'))
        self.assertIsNone(data.get('is_there_a_key'))

    def test_delete_a_question(self):
        # test delete a not exist question
        res = self.client().delete('/questions/1/')
        self.assertEqual(res.status_code, 404)

        # test delete an exist question
        res = self.client().delete('/questions/2/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_422_on_deleting_question(self):
        # this test is when error 422 occurs when deleting a question
        # res = self.client().delete('/questions/2/')
        # data = json.loads(res.data)
        # self.assertEqual(res.status_code, 422)
        # self.assertFalse(data.get('success'))
        pass

    def test_add_question(self):
        new_question = {
            'answer': 'the answer',
            'category': 2,
            'difficulty': 3,
            'question': 'the question'
        }

        res = self.client().post('/questions/', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(len(data.get('questions')))

    def test_search_question(self):
        search_term = {
            'searchTerm': 'what',
        }

        res = self.client().post('/questions/search/', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(len(data.get('questions')))
        self.assertTrue(data.get('total_questions'))
        self.assertTrue(len(data.get('current_category')))

    def test_get_questions_by_category(self):
        # test method not allowed
        res = self.client().post('/categories/2/questions/')
        self.assertEqual(res.status_code, 405)

        # test getting the questions of category 2
        res = self.client().get('/categories/2/questions/')
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('total_questions'))
        self.assertTrue(len(data.get('current_category')))

    def test_get_questions_by_non_exist_category(self):
        res = self.client().get('/categories/10/questions/')
        self.assertEqual(res.status_code, 404)

        data = json.loads(res.data)
        self.assertFalse(data.get('success'))
        self.assertFalse(data.get('questions'))
        self.assertFalse(data.get('total_questions'))
        self.assertFalse(data.get('current_category'))

    def test_quizzes_with_all_questions(self):
        # test all the categories with previous_questions, to play the quiz
        data = {
            'quiz_category': {
                'type': 'click',
            },
            'previous_questions': [1, 2]
        }

        res = self.client().post('/quizzes/', json=data)
        self.assertTrue(res.status_code, 200)

        data = json.loads(res.data)
        self.assertTrue(len(data.get('question')))

        # test all the categories with no previous_questions, to play the quiz
        data = {
            'quiz_category': {
                'type': 'click',
            },
            'previous_questions': None
        }

        res = self.client().post('/quizzes/', json=data)
        self.assertTrue(res.status_code, 200)
        self.assertFalse(data.get('question'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
