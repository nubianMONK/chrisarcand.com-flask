from flask import Blueprint, request, redirect, render_template, url_for
from app.forms import ContactForm
from app.models import Post

from smtplib import SMTP_SSL as SMTP 
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
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
	return redirect("/static/docs/cpa_resume_web.pdf")


@index.route("/contact", methods=("GET", "POST"))
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Yes, I know this really isn't secure at all, but whatever, for now. 
        # Please don't hack my server and make me spend 20 minutes restoring from backup.
        # That would be irritating.
    	name = form.name.data
    	email = form.email.data
    	phone = form.phone.data
    	msg = MIMEText('Name: ' + name + '\nEmail: ' + email + '\nPhone: ' + phone + '\n\n' + form.body.data)

        msg["From"] = email
        msg["To"] = "chris@chrisarcand.com"
        msg["Subject"] = "NEW EMAIL FROM CHRISARCAND.COM"
        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        p.communicate(msg.as_string())

        return render_template("content/contact.html", submitted=True)
    return render_template("content/contact.html", form=form)
