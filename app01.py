from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from models import db, User
from flask_bcrypt import Bcrypt


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qhJObZdaMjzt3RTHexnlHldtP_WksfAHiJfmPncb3cU'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
bcrypt = Bcrypt(app) 

@app.route('/index/')
def html_index():
    return render_template('index.html')

@app.route('/clothes/')
def html_clothes():
    return render_template('clothes.html')

@app.route('/jacket/')
def html_jacket():
    return render_template('jacket.html')

@app.route('/shoes/')
def html_shoes():
    return render_template('shoes.html')

@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        #email = request.form.get('email')
        response = make_response("Cookie установлен")
        response.set_cookie('name', 'email')
        return redirect(url_for('exit'))
    return render_template('form.html')

@app.route('/exit/', methods=['GET', 'POST'])
def exit():
    if request.method == 'POST':
        name = request.form.get('name')
        #email = request.form.get('email')
        res = make_response("Cookie удалён")
        res.set_cookie('0', '0', max_age=0)
        return f'Hello {name}!'
    return render_template('exit.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(f'{form.password}').decode('utf-8')
        user = User(name = f'{form.name}', surname = f'{form.surname}', email = f'{form.email}', password = f'{hashed_password}')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('submit'))
    return render_template('login.html', form=form)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


if __name__ == '__main__':
    app.run()