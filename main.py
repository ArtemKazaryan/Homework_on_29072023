
# Домашняя работа на 29.07.2023


import os
import sqlite3
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
from DataBase import DataBase

DATABASE = '/tmp/financial.db'
DEBUG = True
SECRET_KEY = '123456789'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({'DATABASE': os.path.join(app.root_path, 'financial.db')})

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with open('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    db_con = connect_db()
    db = DataBase(db_con)
    if request.method == 'POST':
        if len(request.form['date']) > 1:
            flash('Транзакция успешно зарегистрирована!', category='success')
    return render_template("index.html", title='Ввод параметров транзакции', menu=db.get_menu())

@app.route('/about')
def about():
    db_con = connect_db()
    db = DataBase(db_con)
    return render_template("about.html", menu=db.get_menu())

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    db_con = connect_db()
    db = DataBase(db_con)
    context = {}
    if request.method == 'POST':
        if len(request.form['username']) > 1:
            flash('Сообщение отправлено успешно!', category='success')
        else:
            flash('Ошибка отправки!', category='error')
        context = {
            'username': request.form['username'],
            'phone': request.form['phone'],
            'message': request.form['message']
        }
    return render_template("contacts.html", **context, title='Обратная связь', menu=db.get_menu())

@app.route('/profile/<username>')
def profile(username):
    db_con = connect_db()
    db = DataBase(db_con)
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template("profile.html", title=f'Авторизация пользователя {username} уже произведена', menu=db.get_menu())

@app.route('/login', methods=['GET', 'POST'])
def login():
    db_con = connect_db()
    db = DataBase(db_con)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'admin' \
                                  and request.form['password'] == '123456789':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=db.get_menu())

@app.errorhandler(400)
def page_not_found(error):
    return render_template('page404.html', title='Неверный запрос', menu=db.get_menu(), error=error), 400

@app.errorhandler(401)
def page_not_found(error):
    return render_template('page404.html', title='Нет прав', menu=db.get_menu(), error=error), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=db.get_menu(), error=error), 404

if __name__ == '__main__':
    create_db()
    app.run()

