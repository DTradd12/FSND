import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'password', 'localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Is this a new question?",
            "answer": "Yes",
            "difficulty": 1,
            "category": 1,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginate_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_get_paginate_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "Not found")

    def test_delete_question_by_id(self):
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == 9).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_add_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        pass

    def test_422_if_add_question_fails(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        pass

    def test_search_questions(self):
        response = self.client().post('/searchQuestions', json={'searchTerm': 'the'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['categories']))

    def test_search_questions_without_results(self):
        response = self.client().post(
            '/searchQuestions', json={'searchTerm': 'banana sandwich'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "unprocessable")

    def test_play_quiz(self):
        response = self.client().post('/quizzes', json={
            'quiz_category': {'Type': 'Entertainment', 'id': '5'},
            'previous_questions': []
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_play_quiz_with_bad_category(self):
        response = self.client().post('/quizzes', json={
            'quiz_category': {'Type': 'Ballyhoo', 'id': '25'},
            'previous_questions': []
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
