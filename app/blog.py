from flask import Blueprint, request, redirect, render_template, url_for, Markup
from flask.views import MethodView
from app.models import Post, Comment
from flask.ext.mongoengine.wtf import model_form
from markdown import markdown
from bs4 import BeautifulSoup

posts = Blueprint('posts', __name__, template_folder='templates')

# These are called 'pluggable views'. Read about them here: http://flask.pocoo.org/docs/views/
# Basically we have classes instead of just functions for views, similar to Django generic views.
# flask.views.MethodView allows you to map different functions to different types of requests,
# (get(self), post(self), etc) rather than use the methods attribute with an 'if' statement. 
# That's obviously useful for RESTful APIs. 

class ListView(MethodView):
    def get(self):
        posts = Post.objects.all()
        for post in posts:
            soup = BeautifulSoup(post.body)
            post.more = soup.find('more')
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):
    # Dynamically create a form (to be passed to the _form macro) using
    # flask.ext.mongoengine.wtf's model_form. It takes the Comment model (class)
    # and creates the form for you. The template for this page will call
    # render(form) which is the _forms Jinja2 macro, which in turn iterates
    # through the fields of the form, displaying them and their error messages, etc.
    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)
        markup = Markup(post.body)

        context = {
            "post": post,
            "form": form,
            "markup": markup
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        '''
        Handles POST (the comment form on the detail view)
        '''
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))
            
        return render_template('posts/detail.html', **context)

# Register the urls
# TODO: the posts blueprint should have /blog/ set as a prefix so these URL's 
# can be relative to it for modularity. 
posts.add_url_rule('/blog', view_func=ListView.as_view('list'))
posts.add_url_rule('/blog/<slug>/', view_func=DetailView.as_view('detail'))

