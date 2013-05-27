from flask import Blueprint, request, redirect, render_template, url_for

index = Blueprint('index', __name__, template_folder='templates')

@index.route("/")
def home():
	return render_template('base.html')