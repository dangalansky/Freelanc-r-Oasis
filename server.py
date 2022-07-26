import os
import csv
import random
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, URLField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AddCafeForm(FlaskForm):
    cafe = StringField("Cafe Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    open = StringField("Opening Time (i.e. 6AM)", validators=[DataRequired()])
    close = StringField("Closing Time (i.e. 5PM)", validators=[DataRequired()])
    coffee = SelectField("Rate Coffee", choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi = SelectField("WIFI?", choices=['YUP', 'NOPE'])
    photo = FileField("Upload Photo (must be .png!)", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def home():
    with open('data.csv', newline='') as file:
        data = csv.reader(file, delimiter=',')
        list = []
        for row in data:
            list.append(row)
    return render_template('index.html', cafes=list)

@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        num = random.randint(1, 6)
        with open('data.csv', 'a') as file:
            file.write(f'\n{form.cafe.data},{form.address.data},{form.open.data},{form.close.data},{form.coffee.data},{form.wifi.data},{num}')
        file = form.photo.data
        if file and allowed_file(file.filename):
            ext = file.filename.split(".")[1]
            full_filename = (os.path.join(
                app.config['UPLOAD_FOLDER'], f'{form.cafe.data}.{ext}'))
            file.save(full_filename)
            return home()
        else:
            return "Unsupported File Type"
    return render_template("add_cafe.html", form=form)

@app.route('/<cafe>')
def details(cafe):
    cafe = cafe.strip()
    with open('data.csv', newline='') as file:
        data = csv.reader(file, delimiter=',')
        list = []
        for row in data:
            list.append(row)
    return render_template("details.html", cafe=cafe, cafes=list)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
