import secrets
from urllib import request
from random import randint

from flask import render_template, Flask, request, redirect, flash, session
from apps.database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 生成一个 16 字节的随机密钥


@app.route('/')
def index():
    db = Database()
    data = db.read(0)
    return render_template('index.html', data=data)


@app.route('/login')
def login():
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error')  # 从 session 中移除错误消息，避免再次显示

    return render_template('login.html', error=error)


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    db = Database()
    loginEmail = request.form['singin-email']
    loginPassword = request.form['singin-password']

    # 調用登入驗證方法
    loginResult = db.login(loginEmail, loginPassword)

    # 在 checkLogin 路由中
    if loginResult == 'Login successful':
        session.pop('error', None)
        return redirect('/dashboard')   # 重導向回登入頁面
    else:
        flash(loginResult, 'error')  # 將錯誤訊息放入 flash 中，並標記為 'error'
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = Database()
    con = db.connect()

    if request.method == 'POST':
        registerUserName = request.form['register-userName']
        registerPassword = request.form['register-password']
        registerFirstName = request.form['register-firstName']
        registerLastName = request.form['register-lastName']
        registerAddress = request.form['register-address']
        registerPhone = request.form['register-phone']
        registerEmail = request.form['register-email']

        registerResult = db.register(firstName=registerFirstName,
                                     lastName=registerLastName,
                                     displayName=registerUserName,
                                     email=registerEmail,
                                     password=registerPassword,
                                     address=registerAddress,
                                     phone=registerPhone)

        if registerResult == 'Registration successful':
            return redirect('/dashboard')
        else:
            return render_template('login.html', error=registerResult)
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/product')
def product():
    return render_template('product.html')


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
    app.run(debug=True, port=8787, host='0.0.0.0')
