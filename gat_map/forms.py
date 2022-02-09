from wtforms import (StringField, SubmitField, FileField)
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm


class GenerateSiteMapForm(FlaskForm):
    start_page = StringField('URL to generate map',
                             validators=[DataRequired(), URL()],
                             default="https://www.globalapptesting.com")
    submit = SubmitField("Generate site map")


class PathForm(FlaskForm):
    source = StringField('Source URL',
                         validators=[DataRequired(), URL()],
                         default="https://www.globalapptesting.com")
    target = StringField('Target URL',
                         validators=[DataRequired(), URL()],
                         default="https://www.globalapptesting.com/blog/page/6")
    submit = SubmitField('Search for the shortest path')


class UploadForm(FlaskForm):
    start_page = StringField('URL used as start page',
                             validators=[DataRequired(), URL()],
                             default="https://www.globalapptesting.com")
    file = FileField()
    submit = SubmitField('Upload json file from previous analysis')