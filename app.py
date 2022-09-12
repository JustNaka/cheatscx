from ast import NamedExpr
from math import prod
from sqlite3 import enable_shared_cache
from flask import abort, Flask, render_template, url_for, request, redirect, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

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
    screens = db.Column(JSON)

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
                return redirect(url_for('admin'))
        
        return redirect(url_for('login'))       
        
    return render_template("login.html")


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if not g.user:
        abort(403)
    
    category = Category.query.all()
    products = Products.query.all()
    
    
    if request.method == 'POST':
        if 'add_element' in request.form:
            if request.form["type"] == "cat":
                new_id = request.form["new_id"]
                new_name = request.form["new_name"]
                new_cat_name = request.form["new_cat_name"]
                new_starting_price = request.form["new_starting_price"]
                new_image_path = request.form["new_image_path"]
                
                if new_id == "" or new_name == "" or new_cat_name == "" or new_starting_price == "" or new_image_path == "":
                    return redirect(url_for('admin'))
                else:
                    db.session.add(Category(id=new_id, name=new_name, image_path=new_image_path, cat_name=new_cat_name, starting_price=new_starting_price, type="cat"))
                    db.session.commit()
            elif request.form["type"] == "prod":
                new_id = request.form["new_id"]
                new_name = request.form["new_name"]
                new_cat_name = request.form["new_cat_name"]
                new_screens = request.form["new_screens"]
                new_image_path = request.form["new_image_path"]
                
                if new_id == "" or new_name == "" or new_cat_name == "" or new_screens == "" or new_image_path == "":
                    return redirect(url_for('admin'))
                else:
                    db.session.add(Products(id=new_id, name=new_name, image_path=new_image_path, cat_name=new_cat_name, screens=new_screens, type="cat"))
                    db.session.commit()
        elif 'edit_element' in request.form:
            if request.form["type"] == "cat":
                edit_id = request.form["edit_id"]
                edit_name = request.form["edit_name"]
                edit_cat_name = request.form["edit_cat_name"]
                edit_starting_price = request.form["edit_starting_price"]
                edit_image_path = request.form["edit_image_path"]
            
                if edit_id == "" or edit_name == "" or edit_cat_name == "" or edit_starting_price == "" or edit_image_path == "":
                    return redirect(url_for('admin'))
                else:
                    cat = Category.query.filter_by(id=request.form["edit_element"]).first()
                    cat.id = edit_id
                    cat.name = edit_name
                    cat.cat_name = edit_cat_name
                    cat.starting_price = edit_starting_price
                    cat.image_path = edit_image_path
                    db.session.commit()
            elif request.form["type"] == "prod":
                edit_id = request.form["edit_id"]
                edit_name = request.form["edit_name"]
                edit_cat_name = request.form["edit_cat_name"]
                edit_screens = request.form["edit_screens"]
                edit_image_path = request.form["edit_image_path"]
            
                if edit_id == "" or edit_name == "" or edit_cat_name == "" or edit_screens == "" or edit_image_path == "":
                    return redirect(url_for('admin'))
                else:
                    cat = Products.query.filter_by(id=request.form["edit_element"]).first()
                    cat.id = edit_id
                    cat.name = edit_name
                    cat.cat_name = edit_cat_name
                    cat.screens = edit_screens
                    cat.image_path = edit_image_path
                    db.session.commit()
            
                
        return redirect(url_for('admin'))
            
    return render_template("admin.html", all_category=category, all_products=products)


@app.route('/deladmin/<int:delc>')
def deladmin(delc):
    if not g.user:
        abort(403)
    
    category = Category.query.all()
    products = Products.query.all()
    
    del_category = Category.query.filter_by(id=delc).first()
    
    if del_category:
        msg_text = 'Elemento %s rimosso' % str(del_category)
        db.session.delete(del_category)
        db.session.commit()
        flash(msg_text)
    return redirect(url_for('admin'))



if __name__ == "__main__":
    app.run(debug=True)