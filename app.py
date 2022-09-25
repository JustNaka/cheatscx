from importlib.metadata import requires
from flask import abort, Flask, render_template, url_for, request, redirect, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from flask_login import (current_user, LoginManager, login_user, logout_user, login_required)
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "Equindimarlenatornaacasa"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=30)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///category.db'
app.config['SQLALCHEMY_BINDS'] = {
    'category':        'sqlite:///category.db',
    'products':      'sqlite:///products.db',
    'users':      'sqlite:///users.db'
}
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

db = SQLAlchemy(app)

class Category(db.Model):
    __bind_key__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    cat_name = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.id

class Products(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    sub_type = db.Column(JSON)
    requirements = db.Column(JSON)
    features = db.Column(JSON)
    screens = db.Column(JSON)

    def __repr__(self):
        return '<Products %r>' % self.id
 
class Users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_auth = db.Column(db.Boolean, nullable=False, default=False)
    @property
    def is_authenticated(self):
        return(self.is_auth)
    @property
    def is_active(self):
        return(True)
    @property
    def is_anonymous(self):
        return(False)
    def get_id(self):
        return(self.id)


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

@app.route('/product/<string:prod_name>', methods=['POST', 'GET'])
def product(prod_name):
    all_prod = Products.query.filter_by(name=prod_name).first_or_404()
    
    if request.method == 'POST':
        sub_type = request.form['sub_type']
        return redirect(url_for("checkout", prod=all_prod.id, sub_type=sub_type))

    return render_template("product.html", product=all_prod)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username != "" and password != "":
            user = Users.query.filter_by(username=request.form['username']).first()

            if user.password == password:
                user.is_auth = True
                db.session.commit()
                login_user(user, remember=True)
                return redirect("admin")
            else:
                flash('Password Errata')
                redirect(url_for('login'))
        else:
            redirect(url_for('login'))
    
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    user = current_user
    user.is_auth = False
    db.session.commit()
    logout_user()
    return redirect("/")

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
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
                new_requirements = request.form["new_requirements"]
                new_status = request.form["new_status"]
                new_sub_type = request.form["new_sub_type"]
                new_description = request.form["new_description"]
                new_image_path = request.form["new_image_path"]
                new_features = request.form["new_features"]
                
                if new_id == "" or new_name == "" or new_cat_name == "" or new_screens == "" or new_image_path == "" or new_requirements == "" or new_status == "" or new_features == "" or new_sub_type == "" or new_description =="":
                    return redirect(url_for('admin'))
                else:
                    db.session.add(Products(id=new_id, name=new_name, image_path=new_image_path, cat_name=new_cat_name, screens=new_screens, requirements=new_requirements, status=new_status, features=new_features, sub_type=new_sub_type, description=new_description, type="cat"))
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
                edit_requirements = request.form["edit_requirements"]
                edit_status = request.form["edit_status"]
                edit_sub_type = request.form["edit_sub_type"]
                edit_features = request.form["edit_features"]
                edit_description = request.form["edit_description"]
                edit_image_path = request.form["edit_image_path"]
            
                if edit_id == "" or edit_name == "" or edit_cat_name == "" or edit_screens == "" or edit_image_path == "" or edit_requirements == "" or edit_status == "" or edit_features == "" or edit_sub_type == "" or edit_description == "":
                    return redirect(url_for('admin'))
                else:
                    cat = Products.query.filter_by(id=request.form["edit_element"]).first()
                    cat.id = edit_id
                    cat.name = edit_name
                    cat.cat_name = edit_cat_name
                    cat.screens = edit_screens
                    cat.status = edit_status
                    cat.requirements = edit_requirements
                    cat.features = edit_features
                    cat.image_path = edit_image_path
                    cat.sub_type = edit_sub_type
                    cat.description = edit_description
                    db.session.commit()
            
                
        return redirect(url_for('admin'))
            
    return render_template("admin.html", all_category=category, all_products=products)

@app.route('/deladmin/<int:delid>/<string:origin>/<string:type>')
@login_required
def deladmin(delid, origin, type):
    if origin != 'admin':
        abort(404)


    if type == 'cat':
        del_category = Category.query.filter_by(id=delid).first()
        
        if del_category:
            msg_text = 'Elemento %s rimosso' % str(del_category)
            db.session.delete(del_category)
            db.session.commit()
            flash(msg_text)
    elif type == 'prod':
        del_category = Products.query.filter_by(id=delid).first()
        
        if del_category:
            msg_text = 'Elemento %s rimosso' % str(del_category)
            db.session.delete(del_category)
            db.session.commit()
            flash(msg_text)        
            
    return redirect(url_for('admin'))

# /checkout?prod=1&sub_type=""
@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    prod = request.args.get("prod")
    sub_type = request.args.get("sub_type")
    
    if prod == None or sub_type == None:
        return redirect(url_for(".index"))
    
    product = Products.query.filter_by(id=prod).first_or_404()
    
    
    return render_template('checkout.html', product=product)

return_value = {"rust": "", "apex": "", "dead": "", "dayz": "", "tarkov": "", "cycle": "", "valorant": "", "gta": "", "fivem": "", "last_update": ""}  
def web_scraping():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Inizio Web Scraping ore: ", dt_string)
    return_value["last_update"] = dt_string
    
    collapse_games = ["rust-en-full", "apex", "dbd-en", "dayz-en", "tarkov-en", "cycle-en", "valorant-en"]
    our_games = ["rust", "apex", "dead", "dayz", "tarkov", "cycle", "valorant"]
    games_status = []
    base_url = "https://collapse.fun/games/rust-en-full/"
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    productMenu__info = soup.find_all("div", class_="productMenu__info")

    for i in productMenu__info:
        productMenu__swiper = i.find_all("div", class_="productMenu__swiper")    
        for y in productMenu__swiper:
            swiper_wrapper = y.find_all("div", class_="swiper-wrapper")
            for j in swiper_wrapper:
                swiper_slide = j.find_all("div", class_="swiper-slide")
                for k in swiper_slide:
                    productInfoFeature__value = k.find_all("span", class_="productInfoFeature__value")
                    games_status.append(productInfoFeature__value[0].text)
    
    for i in our_games:
        cat = Products.query.filter_by(cat_name=i).first()
        if cat.name == "RUST FULL":
            rustlite= Products.query.filter_by(name="RUST LITE").first()
            rustlite.status = games_status[our_games.index(i)]
        cat.status = games_status[our_games.index(i)]
        db.session.commit()
    
    print("Web Scraping eseguito con successo! \n")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Inizio Web Scraping ore: ", dt_string)
    
    collapse_games = ["rust-en-full", "apex", "dbd-en", "dayz-en", "tarkov-en", "cycle-en", "valorant-en"]
    our_games = ["rust", "apex", "dead", "dayz", "tarkov", "cycle", "valorant"]
    games_status = []
    base_url = "https://collapse.fun/games/rust-en-full/"
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    productMenu__info = soup.find_all("div", class_="productMenu__info")

    for i in productMenu__info:
        productMenu__swiper = i.find_all("div", class_="productMenu__swiper")    
        for y in productMenu__swiper:
            swiper_wrapper = y.find_all("div", class_="swiper-wrapper")
            for j in swiper_wrapper:
                swiper_slide = j.find_all("div", class_="swiper-slide")
                for k in swiper_slide:
                    productInfoFeature__value = k.find_all("span", class_="productInfoFeature__value")
                    games_status.append(productInfoFeature__value[0].text)
    
    for i in our_games:
        cat = Category.query.filter_by(cat_name=i).first()
        cat.status = games_status[our_games.index(i)]
        db.session.commit()
    
    print("Web Scraping eseguito con successo! \n")

scheduler = BackgroundScheduler()
scheduler.add_job(func=web_scraping, trigger="interval", minutes=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    #web_scraping()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    
