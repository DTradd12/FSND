import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from projects.capstone.starter.app import create_app
from database.models import setup_db
from auth.auth import AuthError, requires_auth

assistant_token = 'needed'  # @ TODO
director_token = 'needed'  # @ TODO
producer_token = 'needed'  # @ TODO


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.APP = create_app()
        self.client = self.APP.test_client
        self.database_path = "postgresql://postgres:password@localhost:5432/castingagency_test"
        setup_db(self.APP, self.database_path)

        self.headers_casting_assistant = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {assistant_token}"
        }
        self.headers_casting_director = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {director_token}"
        }
        self.headers_executive_producer = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {producer_token}"
        }

        self.new_actor = {
            "name": "Actor TestName",
            "age": 100,
            "gender": "Male/Female"
        }
        self.new_movie = {
            "title": "Movie TestTitle",
            "release_date": "5/18/1990"
        }

        with self.APP.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.APP)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_movies_and_actors(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_add_actor(self):
        response = self.client().post('/actors/create', json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['actor'])

    def test_add_movie(self):
        response = self.client().post('/movies/create', json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['movie'])

    # def test_delete_movie_by_id(self):
    #     response = self.client().delete('/movies/1')
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)
    #
    # def test_delete_actor_by_id(self):
    #     response = self.client().delete('/actors/1')
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted'], 1)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_add_movie_fails(self):
        response = self.client().post('/movies', json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_422_if_add_actor_fails(self):
        response = self.client().post('/actors', json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_new_actor_casting_assistant(self):
        res = self.client().post('/actors', headers=self.headers_casting_assistant,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    # def test_create_new_movies_executive_producer(self):
    #     res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(self.executive_producer)},
    #                              json=self.movies)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #
    # def test_create_new_movies_casting_assistant(self):
    #     res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(self.casting_assistant)},
    #                              json=self.movies)
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401,
    #                      self.assertEqual(data['message'], {
    #                          'code': 'unauthorized', 'description':
    #                              'Permission not found.'})


#     @TODO add tests for authorization failures

if __name__ == "__main__":
    unittest.main()
