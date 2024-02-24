from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class NewBoardForm(FlaskForm):
    board_name = StringField("Board name", render_kw={"placeholder": "Board name"}, validators=[InputRequired(), Length(min=2, max=50)])
    board_description = StringField("Board description", render_kw={"placeholder": "Board description"}, validators=[Length(min=0, max=150)])
    board_tag = StringField("Board tag", render_kw={"placeholder": "Board tag"}, validators=[Length(min=1, max=5)])
    board_category = SelectField("Board category", coerce=int)
    is_nsfw = BooleanField("NSFW")
    is_locked = BooleanField("Locked")

    create_board = SubmitField("Create new board")


class NewCategoryForm(FlaskForm):
    category_name = StringField("Category name", validators=[InputRequired(), Length(min=1, max=50)])

    create_category = SubmitField("Create new category")


class NewPostForm(FlaskForm):
    post_title = StringField("Title", render_kw={"placeholder": "Title", "id": "pH"}, validators=[Length(min=0, max=150)])
    post_text = TextAreaField("Text", render_kw={"placeholder": "Text", "id": "pT"}, validators=[Length(min=0, max=450)])
    create_post = SubmitField("+ Post")
