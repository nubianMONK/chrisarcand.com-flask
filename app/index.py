from flask import Blueprint, request, redirect, render_template, url_for
from app.forms import ContactForm

index = Blueprint('index', __name__, template_folder='templates')

@index.route("/")
def home():
	return render_template('content/index.html')

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
        return redirect(url_for("index.home"))
    return render_template("content/contact.html", form=form)
