from ast import NamedExpr
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///category.db'
app.config['SQLALCHEMY_BINDS'] = {
    'category':        'sqlite:///category.db',
    'products':      'sqlite:///products.db'
}
db = SQLAlchemy(app)

class Category(db.Model):
    __bind_key__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    cat_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.id

class Products(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Products %r>' % self.id




@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_category = request.form['product_category']
        
        print("sUCA MERDE " + product_category)
        all_products = Products.query.filter_by(cat_name=product_category).all()
        return render_template("home.html", products=all_products)
        
    else:
        all_products = Category.query.all()
        return render_template("home.html", products=all_products)




#@app.route('/admin', methods=['POST', 'GET'])
#def sucs():
#    if request.method == 'POST':
#        task_content = request.form['content']
#        new_task = Category(content=task_content)
#        
#        try:
#            db.session.add(new_task)
#            db.session.commit()
#            return redirect("/")
#        except:
#            return 'Errorr'
#        
#    else:
#        tasks = Category.query.order_by(Category.date_created).all()
#        return render_template("base.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
    
    