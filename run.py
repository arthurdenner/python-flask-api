from database.db import initialize_db
from resources.routes import initialize_routes
from app import app, api

initialize_db(app)
initialize_routes(api)

app.run()
