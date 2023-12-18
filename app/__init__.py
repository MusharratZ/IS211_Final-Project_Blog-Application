from flask import Flask
from app.extensions import db
from config import Config
from flask_login import LoginManager
from app.models.user import User
from app.models.post import Post
from flask import render_template
from flask_login import current_user, login_required


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SECRET_KEY"] = "my_secret_key"
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"

    # Initialize Flask extensions here
    db.init_app(app)
    # Register blueprints here
    # for main
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    # for posts
    from app.posts import bp as posts_bp

    app.register_blueprint(posts_bp, url_prefix="/posts")

    # for auth
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # flask_login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        posts = Post.query.filter_by(user=current_user).all()
        return render_template("posts/dashboard.html", posts=posts)

    return app
