from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import Post, Comment
from flask.ext.mongoengine.wtf import model_form

posts = Blueprint('posts', __name__, template_folder='templates')

# These are called 'pluggable views'. Read about them here: http://flask.pocoo.org/docs/views/
# Basically we have classes instead of just functions for views, similar to Django generic views.
# flask.views.MethodView allows you to map different functions to different types of requests,
# (get(self), post(self), etc) rather than use the methods attribute with an 'if' statement. 
# That's obviously useful for RESTful APIs. 

class ListView(MethodView):
    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):
    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
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
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))