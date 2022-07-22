from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
app.secret_key = 'gh_Bjdl4(kdasdfkJn.)mQ'
Bootstrap(app)


class AddCafe(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    photo = URLField(label='Photo Link URL:', validators=[DataRequired()])
    location = URLField(label='Google Maps URL:', validators=[DataRequired()])
    open = StringField(label='Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField(label='Closing Time e.g. 5PM', validators=[DataRequired()])
    coffee = SelectField(label='Rate Coffee Quality', choices=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])
    wifi = SelectField(label='WIFI?', choices=['YUP!', 'NOPE'])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    # cafe_form = AddCafe()
    return render_template('index.html')


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
    app.run(debug=True)
