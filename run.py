import secrets
from urllib import request

from flask import render_template, Flask, request, redirect, flash, session
from apps.database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 生成一个 16 字节的随机密钥


@app.route('/')
def index():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('index.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        username = None
        return render_template('index.html',
                               username=username,
                               total_quantity=0,
                               total_price=0,
                               products=products)


@app.route('/shop')
def shop():
    db = Database()
    products = db.getAllProductsInfo()
    unique_categories = set()  # Create a set to store unique categories
    categoryCheckbox = request.args.get('categoryCheckbox')  # 获取传递的 categoryCheckbox

    # Iterate through products and add unique categories to the set
    for key, product in products.items():
        unique_categories.add(product['category'])
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('shop.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products,
                               unique_categories=unique_categories,
                               categoryCheckbox=categoryCheckbox)
    else:
        username = None
        return render_template('shop.html',
                               username=username,
                               total_quantity=0,
                               total_price=0,
                               products=products,
                               unique_categories=unique_categories,
                               categoryCheckbox=categoryCheckbox)


@app.route('/product')
def product():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('product.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        username = None
        return render_template('product.html',
                               username=username,
                               products=products,
                               productId=1)


@app.route('/product/<int:productId>')
def productPage(productId):
    db = Database()
    # 获取特定产品的信息
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('product.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products,
                               productId=productId)
    else:
        username = None
        return render_template('product.html',
                               username=username,
                               total_quantity=0,
                               total_price=0,
                               products=products,
                               productId=productId)


@app.route('/checkout')
def checkout():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('checkout.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        return redirect('login')


@app.route('/checkoutOrder', methods=['POST'])
def checkoutOrder():
    db = Database()
    if 'username' in session:
        if request.method == 'POST':
            username = session.get('username')
            orderFirstName = request.form['first-name']
            orderLastName = request.form['last-name']
            orderAddress = request.form['address']
            orderPhoneNumber = request.form['phone-number']
            orderEmail = request.form['email']
            orderNote = request.form['note']

            addOrderResult = db.addOrderAndDeleteUserShoppingCart(firstName=orderFirstName,
                                                                  lastName=orderLastName,
                                                                  address=orderAddress,
                                                                  phoneNumber=orderPhoneNumber,
                                                                  email=orderEmail,
                                                                  note=orderNote,
                                                                  username=username)

            if addOrderResult != None:
                return redirect('/dashboard')
            else:
                flash(addOrderResult, 'error')  # 將錯誤訊息放入 flash 中，並標記為 'error'
                return redirect('/checkout')


@app.route('/cart')
def cart():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('cart.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        return redirect('/login')


# TODO 非用戶無法加入購物車邏輯
@app.route('/addToShoppingCart', methods=['GET', 'POST'])
def addToShoppingCart():
    if 'username' in session:
        if request.method == 'POST':
            db = Database()
            productId = request.form['productId']
            quantity = request.form['quantity']
            if productId != 0:
                username = session.get('username')
                added_to_cart = db.addToShoppingCart(username, productId, quantity)  # 调用向购物车添加商品的方法
                if added_to_cart != 0:
                    return redirect('/cart')  # 添加成功后重定向到首页或其他页面
                else:
                    flash('Failed to add product to cart. Please try again.', 'error')
                    return 'Failed to add product to cart.'  # 添加失败的消息
            else:
                flash('Invalid product ID or quantity.', 'error')
                return 'Product ID not provided.'  # 如果没有提供产品ID，则返回错误消息
    else:
        error = ''
        if 'error' in session:
            error = session['error']
            session.pop('error')  # 从 session 中移除错误消息，避免再次显示

        return render_template('login.html', error=error)


@app.route('/deleteUserShoppingCart', methods=['GET', 'POST'])
def deleteUserShoppingCart():
    if 'username' in session:
        if request.method == 'POST':
            db = Database()
            productId = request.form['productId']
            if productId != 0:
                username = session.get('username')
                deleted_from_cart = db.deleteUserShoppingCart(username, productId)
                if deleted_from_cart != 0:
                    return redirect('/cart')
                else:
                    flash('Failed to delete product from cart. Please try again.', 'error')
                    return 'Failed to delete product from cart.'
            else:
                flash('Invalid product ID.', 'error')
                return 'Invalid product ID.'
        else:
            # Handle GET request (if needed)
            # For example, display a message or redirect to another page
            pass
    else:
        error = session.get('error', '')
        session.pop('error', None)
        return render_template('login.html', error=error)


@app.route('/about')
def about():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('about.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        username = None
        return render_template('about.html', username=username, total_quantity=0, total_price=0, products=products)


@app.route('/contact')
def contact():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('contact.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        username = None
        return render_template('contact.html',
                               username=username,
                               total_quantity=0,
                               total_price=0,
                               products=products)


@app.route('/faq')
def faq():
    db = Database()
    products = db.getAllProductsInfo()
    if 'username' in session:
        username = session['username']
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        total_quantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)  # Calculate total quantity
        total_price = db.getUserShoppingCartTotalPriceByUsername(username=username)
        return render_template('faq.html',
                               username=username,
                               total_quantity=total_quantity,
                               total_price=total_price,
                               shopping_cart=shopping_cart,
                               products=products)
    else:
        username = None
        return render_template('faq.html',
                               username=username,
                               total_quantity=0,
                               total_price=0,
                               products=products)


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
    session.pop('username', None)
    return redirect('/login')  # 注销后重定向到登录页面


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    db = Database()
    loginEmail = request.form['singin-email']
    loginPassword = request.form['singin-password']
    username = db.getUsernameByEmail(loginEmail)
    # 調用登入驗證方法
    loginResult = db.login(loginEmail, loginPassword)
    # 在 checkLogin 路由中
    if loginResult == 'Login successful':
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
            session['username'] = registerUserName
            return redirect('/dashboard')
        elif registerResult == 'User with this email already exists':
            flash('This email is already registered.', 'error')
            return redirect('/login')
        elif registerResult == 'This username already exists':
            flash('This username already exists.', 'error')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/dashboard')
def dashboard():
    db = Database()

    # 对于返回类型为 () 的参数
    products = db.getAllProductsInfo()

    # 对于返回类型为 None 的参数
    username = session.get('username')
    if username:
        orders = db.getUserOrdersByUsername(username=username)
        shopping_cart = db.getUserShoppingCartByUsername(username=username)
        shoppingcartTotalQuantity = db.getUserShoppingCartTotalQuantityByUsername(username=username)
        shoppingcartTotalPrice = db.getUserShoppingCartTotalPriceByUsername(username=username)
        orderTotalPrice = db.getUserOrderTotalPriceByUsername(username=username)
        productsName = db.getAllProductsName()
        memberInformation = db.getUserInformationByUsername(username=username)
        print(orders, shopping_cart, shoppingcartTotalQuantity, shoppingcartTotalPrice, orderTotalPrice)

        return render_template('dashboard.html',
                               username=username,
                               total_quantity=shoppingcartTotalQuantity,
                               total_price=shoppingcartTotalPrice,
                               shopping_cart=shopping_cart,
                               products=products,
                               orders=orders,
                               productsName=productsName,
                               orderTotalPrice=orderTotalPrice,
                               memberInformation=memberInformation)
    else:
        return render_template('login.html')


@app.route('/editMemberInformation', methods=['GET', 'POST'])
def editMemberInformation():
    db = Database()
    if 'username' in session:
        username = session['username']

        if request.method == 'POST':
            firstName = request.form['first-name']
            lastName = request.form['last-name']
            displayName = request.form['display-name']
            email = request.form['email']
            oldPassword = request.form['old-password']
            newPassword = request.form['new-password']
            confirmNewPassword = request.form['confirm-new-password']

            if newPassword is None and confirmNewPassword is None:
                editUserInformationResult = db.editUserInformationByUsername(username=username,
                                                                             firstName=firstName,
                                                                             lastName=lastName,
                                                                             displayName=displayName,
                                                                             email=email,
                                                                             oldPassword=oldPassword)
                if editUserInformationResult is True:
                    flash("Information updated successfully, please login again.", 'success')
                    session.pop('username')
                    return redirect('/login')
                else:
                    flash("Failed to update information.", 'error')
                    return redirect('/dashboard')
            else:
                userPassword = db.getUserInformationByUsername(username=username)[5]
                # Verify old password before making any changes
                if oldPassword != userPassword:
                    flash("Incorrect password.", 'error')
                    return redirect('/dashboard')
                else:
                    # Ensure to handle new password securely, such as hashing before storing in the database
                    # Add logic here to update the user's information, including handling the password change securely
                    editUserInformationResult = db.editUserInformationByUsername(username=username,
                                                                                 firstName=firstName,
                                                                                 lastName=lastName,
                                                                                 displayName=displayName,
                                                                                 email=email,
                                                                                 oldPassword=oldPassword,
                                                                                 newPassword=newPassword,
                                                                                 confirmNewPassword=confirmNewPassword)
                    if editUserInformationResult is True:
                        flash("Information updated successfully, please login again.", 'success')
                        session.pop('username')
                        return redirect('/login')
                    else:
                        flash("Failed to update information.", 'error')
                        return redirect('/dashboard')

        else:
            # Handle GET request, render the form for editing member information
            return redirect('/dashboard')
    else:
        return redirect('login.html')  # Redirect to login page if the user is not logged in


@app.errorhandler(404)
def page_not_found(e):
    if 'username' in session:
        username = session['username']
        return render_template('404.html', username=username)
    else:
        return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
