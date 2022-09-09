from ast import NamedExpr
from math import prod
from flask import abort, Flask, render_template, url_for, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Equindimarlenatornaacasa"

@app.before_request
def before_request():
    if 'user_id' in session:
        all_users = Users.query.all()
        
        for x in all_users:
            if x.id == session['user_id']:
                g.user = x.username
    else:
        g.user = None

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///category.db'
app.config['SQLALCHEMY_BINDS'] = {
    'category':        'sqlite:///category.db',
    'products':      'sqlite:///products.db',
    'users':      'sqlite:///users.db'
}
db = SQLAlchemy(app)

class Category(db.Model):
    __bind_key__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    cat_name = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.id

class Products(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.id

class Users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_category = request.form['product_category']

        if product_category == "home":
            all_products = Category.query.all()
        else:
            all_products = Products.query.filter_by(cat_name=product_category).all()
    else:
        all_products = Category.query.all()
        
    return render_template("home.html", products=all_products)


@app.route('/product/<string:prod_name>')
def product(prod_name):
    all_prod = Products.query.filter_by(name=prod_name).first_or_404()

    return render_template("product.html", product=all_prod)




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        
        username = request.form['password']
        password = request.form['password']
        
        all_users = Users.query.all()

        for x in all_users:
            if x != None and x.password == password:
                session['user_id'] = x.id
                return redirect(url_for('profile'))
        
        return redirect(url_for('login'))       
        
    return render_template("login.html")


@app.route('/profile')
def profile():
    if not g.user:
        abort(403)
    return render_template("profile.html")





if __name__ == "__main__":
    app.run(debug=True)