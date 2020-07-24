import json

from flask_jwt_extended import create_access_token
from tests.base_case import BaseCase


class TestUserLogin(BaseCase):
    def test_successful_create_movie(self):
        # Given
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('/api/auth/signup',
                      headers={"Content-Type": "application/json"},
                      data=user_payload)
        response = self.app.post('/api/auth/login',
                                 headers={"Content-Type": "application/json"},
                                 data=user_payload)
        login_token = response.json['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        # When
        response = self.app.post('/api/movies',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(movie_payload))

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_failed_create_movie_without_token(self):
        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        # When
        response = self.app.post('/api/movies',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(movie_payload))

        # Then
        self.assertEqual('Missing Authorization Header', response.json['msg'])
        self.assertEqual(401, response.status_code)

    def test_failed_create_movie_with_duplicate_name(self):
        # Given
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('/api/auth/signup',
                      headers={"Content-Type": "application/json"},
                      data=user_payload)
        response = self.app.post('/api/auth/login',
                                 headers={"Content-Type": "application/json"},
                                 data=user_payload)
        login_token = response.json['token']

        movie_payload = {
            "name": "Star Wars: The Rise of Skywalker",
            "casts": ["Daisy Ridley", "Adam Driver"],
            "genres": ["Fantasy", "Sci-fi"]
        }

        # When
        self.app.post('/api/movies',
                      headers={"Content-Type": "application/json",
                               "Authorization": f"Bearer {login_token}"},
                      data=json.dumps(movie_payload))
        response = self.app.post('/api/movies',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(movie_payload))

        # Then
        self.assertEqual('Movie with given name already exists',
                         response.json['message'])
        self.assertEqual(400, response.status_code)
