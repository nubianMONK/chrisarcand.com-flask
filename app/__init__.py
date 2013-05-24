from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "chrisarcand-flask-site"}
app.config["SECRET_KEY"] = "thisisasupersecretpassword1!"

# MongoEngine is an Object-Document Mapper for using Python with MongoDB
# http://docs.mongoengine.org/en/latest/apireference.html
db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from app.views import posts
    from app.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == '__main__':
    app.run()