from flask import (render_template, request, Blueprint, make_response,g,current_app,
redirect, url_for)
from flaskapp.models import Post,User
from flask_login import current_user, login_required
from datetime import datetime
from flaskapp import db
from flask import g
from flaskapp.main.forms import Searcher

main = Blueprint('main', __name__)


@main.route('/pastpapers')
def pastpaper():
    return render_template("pastpapers.html")

#This is the homepage subroutine. 
@main.route('/')
@main.route('/home')
def HomePage():
    page = request.args.get('page', 1, type = int)
    showed_followed = False
    if current_user.is_authenticated:
        showed_followed = bool(request.cookies.get('showed_followed', ''))
    if showed_followed:
        query= current_user.followed_posts
    else: 
        query = Post.query
    pagination = query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5, 
            error_out = False)
    posts = pagination.items
    return render_template("HomePage.html", posts =posts, showed_followed = showed_followed , 
        pagination = pagination)

#This is where all the posts submitted by users are sent to . This is the post area
@main.route("/compscipost",methods=['GET', 'POST'])
def compscipost():
	page = request.args.get('page', 1, type = int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
	return render_template("compscipost.html", posts = posts)

#Subroutine for about page
@main.route("/about")
def about():
    return render_template("About.html", title = 'About')

#Subroutine for contact page 
@main.route("/contact")
def contact():
    return render_template("contact.html", title = 'Contact Us')

#This subroutine shows 5 posts from post area to homepage.
@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.HomePage')))
    resp.set_cookie('showed_followed', '' , max_age = 30*24*60*60)
    return resp

#This subroutine shows 5 posts from post area to homepage.
@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.HomePage')))
    resp.set_cookie('showed_followed', '1', max_age = 30*24*60*60)
    return resp

#This is for the search function
@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = Searcher()

#This is the searh subroutine.
@main.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.HomePage'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)