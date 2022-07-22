import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import csv
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/Users/dangalansky/Dropbox/pythonProject/Portfolio/Freelance-Oasis/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'gh_Bjdl4(kdasdfkJn.)mQ'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
WTF_CSRF_SECRET_KEY = 'gh_Bjdl4(kdasdfkJn.)mQ'
Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AddCafe(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    photo = FileField(label='Photo Upload', validators=[FileRequired()])
    location = URLField(label='Google Maps URL:', validators=[DataRequired()])
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField(label='Closing Time e.g. 5PM', validators=[DataRequired()])
    coffee = SelectField(label='Rate Coffee Quality', choices=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])
    wifi = SelectField(label='WIFI?', choices=['YUP!', 'NOPE'])
    submit = SubmitField('Submit')

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/elements', methods=['GET', 'POST'])
def elements():
    form = PhotoForm()
    if form.validate_on_submit():
        # f = form.photo.data
        # filename = secure_filename(f.filename)
        # f.save(os.path.join(
        #     app.config['UPLOAD_FOLDER'], filename
        # ))
        return redirect(url_for('home'))

    return render_template('elements.html', form=form)


@app.route('/cafe_list')
def cafe_list():
    with open('data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafe_list.html', cafes=list_of_rows)


@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafe()
    if form.validate_on_submit():
        with open('data.csv', 'a') as file:
            file.write(
                f'\n{form.cafe.data},{form.photo.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee.data},{form.wifi.data}')
        return cafe_list()
    return render_template('add_cafe.html', form=form)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
