from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post, Comment


forum = Blueprint('forum', __name__)


@forum.route('/forum')
def forum_home():
    posts = Post.query.all()
    return render_template('forum.html', posts=posts)


@forum.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and Content cannot be empty!', category='error')
        else:
            new_post = Post(title=title, content=content,
                            user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('forum.forum_home'))

    return render_template('create_post.html')


@forum.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()

    if request.method == 'POST':
        comment_content = request.form.get('comment')
        if comment_content:
            new_comment = Comment(content=comment_content,
                                  user_id=current_user.id, post_id=post.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', category='success')
            return redirect(url_for('forum.post_detail', post_id=post.id))

    return render_template('post_detail.html', post=post, comments=comments)
