from operator import or_
import os
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
from webforms import EditForm,RegistrationForm,LoginForm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bcrypt = Bcrypt(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    total = db.Column(db.Integer, nullable=True, default=0)  # Добавлено значение по умолчанию


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

def search_items(search_term):
    conditions = [
        or_(
            db.func.lower(Item.title).startswith(db.func.lower(search_term)),
            db.func.lower(Item.details).startswith(db.func.lower(search_term))
        )
        for char in search_term
    ]
    return Item.query.filter(*conditions).order_by(Item.price).all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/magazin", methods=["GET", "POST"])
def magazin():
    if request.method == "POST":
        search_term = request.form.get("searched", "")
        search_term = search_term.capitalize()  # Сделаем первую букву заглавной
        items = search_items(search_term)
    else:
        items = Item.query.order_by(Item.price).all()

    return render_template("magazin.html", data=items)

@app.route('/about')
def about():
    return render_template('about.html')
#регистрация для сайта


@app.route('/register', methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.username.data,lastname=form.lastname.data,email = form.email.data,phone = form.phone.data,city = form.city.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Заебись все работает')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login successful!', 'success')
            session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
            return redirect(url_for('profile'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = Users.query.get(user_id)
        return render_template('profile.html', title='Profile', user=user)
    else:
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

@app.route('/details/<int:id>')
def item_details(id):
    item = Item.query.get(id)
    return render_template('details.html', item=item)


@app.route('/buy/<int:id>')
def item_buy(id):
    return str(id)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        details = request.form['details']
        img = request.form['img']
        total = request.form['total']

        item = Item(title=title, price=price, details=details, img=img, total=total)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')


@app.route('/update', methods=['GET'])
def update():
    items = Item.query.all()
    return render_template('update.html', items=items)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Item.query.get(id)
    form = EditForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        return redirect(url_for('update'))

    return render_template('edit.html', form=form, item=item)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    item = Item.query.get(id)

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect(url_for('update'))


if __name__ == '__main__':
    app.run(debug=True)
