chrisarcand.com-v4
==================

My personal website, version 4: Using the Flask microframework (Python)

MongoEngine backend based on Ross Lawley's flask-tumblelog (https://github.com/rozza/flask-tumblelog)

If you really want to launch this locally (I guess you're a big fan?):

1) You must have pip installed.

  a) Use google.com (RTFM)

2) You should really have a virtualenv set up.

  a) When virtualenv is installed (RTFM), make an environment: Run 'virtualenv --no-site-packages env'

  b) Activate the environment: Run 'source env/bin/activate'

3) Install required Python libraries: Run 'pip install -r requirements.pip'

4) You must have mongodb installed. If you're running OSX, use Homebrew. Run 'brew install mongodb'

5) Make sure mongodb is running (Run 'mongod')

6) Run the server (Flask's built in development server, don't use for production) (Run 'python manage.py runserver')
