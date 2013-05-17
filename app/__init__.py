from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "chrisarcand-flask-site"}
app.config["SECRET_KEY"] = "thisisasupersecretpassword1!"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()