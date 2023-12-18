from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms import (
    SelectField,
    TextAreaField,
    FileField,
)
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileAllowed, FileRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), InputRequired()])
    category_id = SelectField(
        "Category",
        coerce=int,
        validators=[DataRequired(), InputRequired()],
        choices=[],  # Add choices dynamically in your route
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), InputRequired()]
    )
    image = FileField(
        "Image",
        validators=[
            FileAllowed(["jpg", "png"], "Images only!"),
            InputRequired(),
            FileRequired(),
        ],
    )
    is_published = BooleanField("Publish", validators=[InputRequired()])
