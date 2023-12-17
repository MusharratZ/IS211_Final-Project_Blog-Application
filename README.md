# IS211_Final-Project_Blog-Application
For requirement 2 
        "I should be able to checkout your project repository, run pythonapp.pyand expect a working
        version of your project. Opening a web browser to the application main URL should have it bring up
        your project."

Use project/app/__init__.py instead

The project structure
1 For models  move into --> project/app/models
There are three models 
User 
->has four fields :id ,username,email and password
Category
->has three fields :id title and description
Post
->has ten fields:
    id --> primary key
    user_id = --> user foreign key
    user = --> for relaship
    title --> post title
    category_id -->catergory relaship
    category = db.relationship("Category", backref="categories")
    description --> post description
    image -->post image
    is_published boolean to publish and unpublish
    created_at --> shows time post was created


    How it works
    For new user:
    New users can view posts, post details , post from a certain cetegory or user. For them to add a post they will have first to create an account by registering to the system.
    For users with accounts.
    These users can add delete and edit their posts.
