# from flask import render_template
from app.posts import bp
from app.extensions import db
from app.models.post import Post, Category
from app.models.user import User
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from flask import send_from_directory
from .forms import PostForm
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename
from sqlalchemy import desc


@bp.route("/")
def index():
    categories = Category.query.all()
    l_posts = (
        Post.query.order_by(desc(Post.created_at))
        .filter_by(is_published=True)
        .limit(3)
        .all()
    )
    posts = (
        Post.query.filter_by(is_published=True).order_by(desc(Post.created_at)).all()
    )
    return render_template(
        "posts/posts.html", posts=posts, l_posts=l_posts, categories=categories
    )


@bp.route("/categories/")
@login_required
def categories():
    categories = Category.query.all()
    # categories = Category.query.all()
    l_posts = (
        Post.query.order_by(desc(Post.created_at))
        .filter_by(is_published=True)
        .limit(3)
        .all()
    )
    return render_template(
        "posts/categories.html", categories=categories, l_posts=l_posts
    )


@bp.route(
    "/categories-post/<int:category_id>/",
)
@login_required
def category_post(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(is_published=True, category=category).all()
    return render_template("posts/post-categories.html", posts=posts)


@bp.route(
    "/user-post/<int:user_id>/",
)
def user_post(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(is_published=True, user=user).all()
    categories = Category.query.all()
    l_posts = (
        Post.query.order_by(desc(Post.created_at))
        .filter_by(is_published=True)
        .limit(3)
        .all()
    )
    return render_template(
        "posts/post-users.html", posts=posts, categories=categories, l_posts=l_posts
    )


@bp.route("/create-category", methods=("GET", "POST"))
@login_required
def create_category():
    if request.method == "POST":
        category = Category(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("posts.create"))
    return render_template("posts/create-category.html")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = PostForm()
    categorys = Category.query.all()
    form.category_id.choices = [(category.id, category.title) for category in categorys]

    if form.validate_on_submit():
        # Create a new post instance and set its attributes

        post = Post()
        form.populate_obj(post)
        post.user_id = (
            current_user.id
        )  # Assuming you are using Flask-Login for user management
        # Handle image upload
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            post.image = filename
        # Add the post to the database and commit the changes
        db.session.add(post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(
            url_for("posts.post_details", post_id=post.id)
        )  # Replace with the actual route

    return render_template("posts/create.html", form=form)


@bp.route("post-details/<int:post_id>/")
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all()
    l_posts = (
        Post.query.filter(Post.id != post_id)
        .order_by(desc(Post.created_at))
        .filter_by(is_published=True)
        .limit(3)
        .all()
    )
    return render_template(
        "posts/post-details.html", post=post, categories=categories, l_posts=l_posts
    )


@bp.route("/update/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the owner of the post
    if current_user.id != post.user_id:
        flash("You do not have permission to edit this post.", "danger")
        return redirect(url_for("index"))

    form = PostForm(obj=post)  # Load existing post data into the form
    categorys = Category.query.all()
    form.category_id.choices = [(category.id, category.title) for category in categorys]

    if form.validate_on_submit():
        form.populate_obj(post)  # Update post attributes with form data

        # Handle image upload
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            post.image = filename

        db.session.commit()  # Commit the changes to the database

        flash("Post updated successfully!", "success")
        return redirect(url_for("posts.post_details", post_id=post.id))

    return render_template("posts/edit.html", form=form, post=post)


@bp.route("/<int:post_id>/delete/", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("dashboard")


@bp.route("/publish/<int:post_id>")
@login_required
def publish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        post.is_published = True
        db.session.commit()
        flash("Post published successfully!", "success")
    else:
        flash("You do not have permission to publish this post.", "danger")
    return redirect(url_for("dashboard"))


@bp.route("/unpublish/<int:post_id>")
@login_required
def unpublish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        post.is_published = False
        db.session.commit()
        flash("Post unpublished successfully!", "success")
    else:
        flash("You do not have permission to unpublish this post.", "danger")
    return redirect(url_for("dashboard"))


@bp.route("/search-results")
def search_results():
    keyword = request.args.get("keyword", "")
    posts = Post.search(keyword)
    return render_template("posts/search.html", keyword=keyword, posts=posts)


@bp.route("/images/<filename>")
def get_image(filename):
    return send_from_directory("app/images", filename)
