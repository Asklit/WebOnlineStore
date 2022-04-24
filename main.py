from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from admin.put_items_to_db import main_add_to_bd
from data import db_session
from data.orders_items import OrdersItems
from data.products import Products
from data.users import User
from data.orders import Orders
from forms.LoginForm import LoginForm
from forms.SearchForm import SearchForm
from forms.payment import Payment
from forms.user import RegisterForm

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
    return render_template('catalog.html', title='Каталог', name_title=name_title, type="all",
                           list_products=list_products, form=form)


@app.route('/catalog/<data>', methods=['post', 'get'])
def catalog_types(data):
    form = SearchForm()
    if form.validate_on_submit():
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
        # filter_data = db_sess.query(Products).filter(Products.title.like(data)).all()
        filter_data = db_sess.query(Products).all()
    if data in ["woman", "man", "kids"]:
        for elem in filter_data:
            list_products.append([elem.title, elem.price, elem.type, elem.image_path, elem.id])
    else:
        for elem in filter_data:
            if name_title.lower() in elem.title.lower():
                list_products.append([elem.title, elem.price, elem.type, elem.image_path, elem.id])
    return render_template('catalog.html', title='Каталог', name_title=name_title, type="all",
                           list_products=list_products, form=form)


@app.route('/add_to_cart/<data>', methods=['post', 'get'])
@login_required
def add_to_cart(data):
    db_sess = db_session.create_session()
    item = OrdersItems()
    id_ord = db_sess.query(Orders).filter(Orders.id_client == current_user.id, Orders.status == "not paid").first()
    item_in_basket = db_sess.query(OrdersItems).filter(OrdersItems.id_order == id_ord.id,
                                                       OrdersItems.id_product == data).scalar()
    if item_in_basket is None:
        item.id_product = data
        item.id_order = id_ord.id
        db_sess.merge(item)
        db_sess.commit()
    else:
        pass
    return redirect("/catalog/")


@app.route('/delete_from_cart/<data>', methods=['post', 'get'])
@login_required
def delete_from_cart(data):
    db_sess = db_session.create_session()
    id_ord = db_sess.query(Orders).filter(Orders.id_client == current_user.id and Orders.status == "not paid").first()
    item_in_basket = db_sess.query(OrdersItems).filter(OrdersItems.id_order == id_ord.id,
                                                       OrdersItems.id_product == data).first()
    if item_in_basket:
        db_sess.delete(item_in_basket)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/basket")


# Корзина
@app.route('/basket', methods=['post', 'get'])
@login_required
def basket():
    form = Payment()
    db_sess = db_session.create_session()
    data = db_sess.query(Orders).filter(Orders.id_client == current_user.id, Orders.status == "not paid").first()
    items = db_sess.query(OrdersItems).filter(OrdersItems.id_order == data.id).all()
    list_items = []
    total = 0
    for i in items:
        products = db_sess.query(Products).filter(Products.id == i.id_product).first()
        total += products.price
        list_items.append(
            [products.title, products.title.split()[-1], products.price, products.type, products.image_path,
             products.id])

    if form.validate_on_submit():
        try:
            if len("".join(form.number_card.data.split())) != 16:
                raise Exception
            int("".join(form.number_card.data.split()))
        except Exception:
            return render_template('basket.html', title='Корзина', list_items=list_items, count=len(list_items),
                                   message="Неправильный номер карты",
                                   total=total, form=form)
        try:
            if int(form.month.data) > 12 or int(form.month.data) < 0:
                raise Exception
            if int(form.year.data) == 0:
                raise Exception
        except Exception:
            return render_template('basket.html', title='Корзина', list_items=list_items, count=len(list_items),
                                   message="Неправильная дата",
                                   total=total, form=form)
        try:
            if int(form.cvv.data) == 0:
                raise Exception
        except Exception:
            return render_template('basket.html', title='Корзина', list_items=list_items, count=len(list_items),
                                   message="Неправильный CVV код",
                                   total=total, form=form)

        order = db_sess.query(Orders).filter(Orders.id_client == current_user.id, Orders.status == "not paid").first()
        order.status = "paid"
        db_sess.commit()

        order = Orders(
            id_client=current_user.id,
        )
        db_sess.add(order)
        db_sess.commit()

        return redirect('/')
    if len(list_items) == 0:
        return render_template('basket.html', title='Корзина', list_items=[], count=len(list_items),
                                   total=total, form=form)
    return render_template('basket.html', title='Корзина', list_items=list_items, count=len(list_items),
                               total=total, form=form)


if __name__ == '__main__':
    db_session.global_init("db/store.db")
    # main_add_to_bd(db_session.create_session())
    app.run(port=8080, host='127.0.0.1', debug=True)
