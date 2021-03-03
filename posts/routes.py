from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Post, Comment, User
from flaskapp.posts.forms import NewPost, NewComment

posts = Blueprint('posts', __name__)


#This subroutine creates a post. 
@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        #Adds Post To DataBase
        flash("Your Post has been posted!", 'success')
        return redirect(url_for('main.compscipost'))
    return render_template('create_post.html', title='New Post', form = form, 
        legend = "New Post ")

#This allows the post to be viewed .
@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = NewComment()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,commenter_author= post,
            comment_author = current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('posts.post', post_id=post.id, page=-1))
    page = request.args.get('page', 1, type = int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.date_posted.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('comments_post.html', post=post, form = form ,
        comments=comments, pagination = pagination)


#This subroutine allows for post to be liked .
@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

#This subroutine allows the specific post of a user to be edited by the user 
@posts.route("/post/<int:post_id>/Edit", methods = ['GET', 'POST'])
@login_required
def edit_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) 
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data =post.content  
    return render_template('create_post.html', title='Edit Post', form = form,
        legend = "Edit Post")

#This subroutine allows the specific post of a user to be deleted by the user.

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.compscipost'))



