import os
import sys

#Set the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_debugtoolbar import DebugToolbarExtension

from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

# Rewrite headers like REMOTE_ADDR and HTTP_HOST so Flask can work with an HTTP proxy (nginx)
# Werkzeug ships a fixer that solves most common setups
app.wsgi_app = ProxyFix(app.wsgi_app)

# MongoDB database name
app.config["MONGODB_SETTINGS"] = {'DB': "chrisarcand-flask-site"}

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["SECRET_KEY"] = "thisISmysuper$%#@secretkey"

# MongoEngine is an Object-Document Mapper for using Python with MongoDB
# http://docs.mongoengine.org/en/latest/apireference.html
db = MongoEngine(app)

#Toolbar extension only shows when debug is on
app.debug = False
toolbar = DebugToolbarExtension(app)

def register_blueprints(app):
    # Prevents circular imports
    from app.blog import posts
    from app.admin import admin
    from app.index import index
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(index)

register_blueprints(app)

if __name__ == '__main__':
    app.run()

