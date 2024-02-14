from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length


class NewBoardForm(FlaskForm):
    board_name = StringField("Board name", validators=[InputRequired(), Length(min=2, max=50)])
    board_description = StringField("Board description", validators=[Length(min=0, max=150)])
    board_tag = StringField("Board tag", validators=[Length(min=1, max=5)])
    create_board = SubmitField("Create new board")
