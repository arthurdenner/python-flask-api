import unittest

from app import app, api
from resources.routes import initialize_routes
from database.db import db, initialize_db


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        if 'mongoengine' not in app.extensions:
            initialize_db(app)
            initialize_routes(api)
        self.db = db.get_db()

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)
