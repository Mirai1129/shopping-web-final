from flask import render_template, Flask
from apps.database import Database


app = Flask(__name__)


@app.route('/')
def index():
    db = Database()
    data = db.read(0)
    return render_template('index.html', data=data)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
