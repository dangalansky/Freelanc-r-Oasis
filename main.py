from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'arandomstring'
Bootstrap(app)

class AddCafe(FlaskForm):
    photo = URLField(label='Enter cafe photo link:')

@app.route('/')
def home():
    cafe_form = AddCafe()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





