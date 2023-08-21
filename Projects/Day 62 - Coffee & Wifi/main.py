from flask import Flask, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)',
                           validators=[DataRequired(), validators.URL()])
    opening_time = StringField('Opening Time (e.g. 8AM)',
                               validators=[DataRequired()])
    closing_time = StringField('Closing Time (e.g. 5:30PM)',
                               validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
                              validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability',
                               choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = list(request.form.values())
        del form_data[0]
        del form_data[-1]
        new_cafe = ','.join(form_data)
        with open('cafe-data.csv', "a", encoding='utf8') as csv_file:
            csv_file.write(f"\n{new_cafe}")
        return redirect('add')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
