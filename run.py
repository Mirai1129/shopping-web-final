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
    if 'username' in session:
        user = session['username']
        data = db.shoppingCartQuantity(username=user)
        price = db.shoppingCartPrice(username=user)
        return render_template('index.html', data=data, user=user, price=price)
    else:
        user = None
        return render_template('index.html', data='', user=user, price=0)


@app.route('/login')
def login():
    if 'username' in session:
        return redirect('/dashboard')
    else:
        error = ''
        if 'error' in session:
            error = session['error']
            session.pop('error')  # 从 session 中移除错误消息，避免再次显示

        return render_template('login.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    # 用户注销，清除会话中的登录信息
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/login')  # 注销后重定向到登录页面


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    db = Database()
    loginEmail = request.form['singin-email']
    loginPassword = request.form['singin-password']
    username = db.getUsername(loginEmail)
    # 調用登入驗證方法
    loginResult = db.login(loginEmail, loginPassword)
    # 在 checkLogin 路由中
    if loginResult == 'Login successful':
        session['loggedIn'] = True
        session['username'] = username
        session.pop('error', None)
        return redirect('/dashboard')  # 重導向回登入頁面
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
            session['loggedIn'] = True
            session['username'] = registerUserName
            return redirect('/dashboard')
        else:
            return render_template('login.html', error=registerResult)
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'loggedIn' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/login')


@app.route('/product')
def product():
    if 'username' in session:
        username = session['username']
        return render_template('product.html', username=username)
    else:
        return render_template('product.html')

@app.route('/shop')
def shop():
    if 'username' in session:
        username = session['username']
        return render_template('shop.html', username=username)
    else:
        return render_template('shop.html')


@app.route('/about')
def about():
    if 'username' in session:
        username = session['username']
        return render_template('about.html', username=username)
    else:
        return render_template('about.html')


@app.route('/contact')
def contact():
    if 'username' in session:
        username = session['username']
        return render_template('contact.html', username=username)
    else:
        return render_template('contact.html')


@app.route('/faq')
def faq():
    if 'username' in session:
        username = session['username']
        return render_template('faq.html', username=username)
    else:
        return render_template('faq.html')


@app.route('/checkout')
def checkout():
    if 'username' in session:
        username = session['username']
        return render_template('checkout.html', username=username)
    else:
        return render_template('checkout.html')


@app.route('/cart')
def cart():
    if 'username' in session:
        username = session['username']
        return render_template('cart.html', username=username)
    else:
        return render_template('cart.html')


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
        username = session['username']
        return render_template('404.html', username=username)
    else:
        return render_template('404.html')



if __name__ == '__main__':
    app.run(debug=True, port=8787, host='0.0.0.0')
