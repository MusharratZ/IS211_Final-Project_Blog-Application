from app.main import bp
from flask import render_template
from app.models.post import Post


@bp.route("/")
def index():
    posts = Post.query.all()[-3:]
    return render_template("home.html", posts=posts)
