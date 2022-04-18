from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import func
from werkzeug.utils import redirect

from data import db_session
from data.products import Products
from data.users import User
from data.orders import Orders
from forms.LoginForm import LoginForm
from forms.SearchForm import SearchForm
from forms.user import RegisterForm
from admin.put_items_to_db import main_add_to_bd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


# начальная страница
@app.route('/', methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/catalog/{form.search_string.data}')
    title = "Модный интернет магазин"
    return render_template('page.html', title=title, form=form)


# регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        order = Orders(
            id_client=user.id,
        )
        db_sess.add(order)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход из аккаунта
@app.route('/logout', methods=['post', 'get'])
@login_required
def logout():
    logout_user()
    return redirect("/")


# О нас
@app.route('/about', methods=['post', 'get'])
def about():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/catalog/{form.search_string.data}')
    return render_template('about_company.html', title='О нас', form=form)


# Каталог
@app.route('/catalog/', methods=['post', 'get'])
def catalog():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/catalog/{form.search_string.data}')
    db_sess = db_session.create_session()
    list_products = []
    name_title = "Популярные товары"
    for elem in db_sess.query(Products).all():
        list_products.append([elem.title, elem.price, elem.type, elem.image_path, elem.id])
    return render_template('catalog.html', title='Каталог', name_title=name_title, type="all", list_products=list_products, form=form)


@app.route('/catalog/<data>', methods=['post', 'get'])
def catalog_types(data):
    form = SearchForm()
    if form.validate_on_submit():
        print(form.catalog.data)
        return redirect(f'/catalog/{form.search_string.data}')
    db_sess = db_session.create_session()
    list_products = []
    if data == "woman":
        name_title = "Женщинам"
        filter_data = db_sess.query(Products).filter(Products.type == data)
    elif data == "man":
        name_title = "Мужчинам"
        filter_data = db_sess.query(Products).filter(Products.type == data)
    elif data == "kids":
        name_title = "Детям и подросткам"
        filter_data = db_sess.query(Products).filter(Products.type == data)
    else:
        name_title = data
        data = "%" + data + "%"
        filter_data = db_sess.query(Products).filter(Products.title.like(data)).all()
    for elem in filter_data:
        list_products.append([elem.title, elem.price, elem.type, elem.image_path, elem.id])
    return render_template('catalog.html', title='Каталог', name_title=name_title, type="all", list_products=list_products, form=form)


@app.route('/catalog/add_to_cart/<data>', methods=['post', 'get'])
@login_required
def add_to_cart(data):
    print(data)
    return redirect("/catalog/")


if __name__ == '__main__':
    db_session.global_init("db/store.db")
    # main_add_to_bd(db_session.create_session())
    app.run(port=8080, host='127.0.0.1')