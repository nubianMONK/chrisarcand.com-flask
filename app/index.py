from flask import Blueprint, request, redirect, render_template, url_for
from app.forms import ContactForm
from app.models import Post

from smtplib import SMTP_SSL as SMTP 
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

index = Blueprint('index', __name__, template_folder='templates')

@index.route("/")
def home():
    posts = Post.objects.all()
    for post in posts:
        soup = BeautifulSoup(post.body)
        post.more = soup.find('more')
    return render_template('content/index.html', posts=posts)

@index.route("/about")
def about():
	return render_template('content/about.html')

@index.route("/projects")
def projects():
	return render_template('content/projects.html')

@index.route("/resume")
def resume():
	return render_template('content/resume.html')


@index.route("/contact", methods=("GET", "POST"))
def contact():
    form = ContactForm()
    if form.validate_on_submit():
    	name = form.name.data
    	email = form.email.data
    	phone = form.phone.data
    	msg = MIMEText(form.body.data)

    	msg['Subject'] = 'New message from ChrisArcand.com'
    	msg['From'] = email
    	# I should totally be using an external config file here, I know. Too lazy, for now...
    	msg['To'] = 'chris@chrisarcand.com'

    	#SMTP SENDER CODE HERE, WILL BE SPECIFIC TO VPS
    	# Make sure you check to make sure the message sent successfully, else warn the user it failed

        return render_template("content/contact.html", submitted=True)
    return render_template("content/contact.html", form=form)
