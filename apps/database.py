import random
import hashlib
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def connect(self):
        return pymysql.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            charset=os.getenv("CHARSET")
        )

    def getUsernameByEmail(self, email):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT displayName FROM shoppingweb.member WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def getUserIdByUsername(self, username):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT memberId FROM shoppingweb.member WHERE displayName = %s", (username))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def shoppingCartQuantityByUsername(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            quantity = cursor.execute(
                "SELECT sc.quantity "
                "FROM shoppingweb.member AS m "
                "JOIN shoppingweb.shoppingcart AS sc ON m.memberId = sc.memberId "
                "WHERE m.displayName = %s", (username,)
            )

            # quantity = cursor.fetchone()[0]  # 获取购物车数量

            return quantity  # 如果数量存在则返回数量，否则返回 0
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return 0  # 返回默认值 0 表示未找到数量
        finally:
            cursor.close()
            con.close()

    def shoppingCartPriceByUsername(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT sc.price "
                "FROM shoppingweb.member AS m "
                "JOIN shoppingweb.shoppingcart AS sc ON m.memberId = sc.memberId "
                "WHERE m.displayName = %s", (username,)
            )
            price = cursor.fetchone()  # Fetch one row from the result set
            if price:
                return price[0]  # Return the first column value (price)
            else:
                return 0  # Return 0 if no price found for the given username
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return 0  # Return 0 if there's a database error
        finally:
            cursor.close()
            con.close()

    def getAllProductsInfo(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM shoppingweb.product")
            products_info = cursor.fetchall()  # Fetch all rows from the result set
            products_dict = {product[0]: {'productId': product[0],
                                          'productName': product[1],
                                          'quantity': product[2],
                                          'price': product[3],
                                          'summary': product[4],
                                          'category': product[5],
                                          'information': product[6],
                                          'introduction': product[7]}
                             for product in
                             products_info}  # Create a dictionary with productId as key and product details as values
            return products_dict  # Return dictionary containing productId and its corresponding product details

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return {}  # Return an empty dictionary if there's a database error
        finally:
            cursor.close()
            con.close()

    def login(self, email, password):
        con = self.connect()
        cursor = con.cursor()
        try:
            if not email or not password:
                return 'Invalid email or password'

            # 使用 Prepared Statement 執行 SQL 查詢，并使用哈希后的密码进行比较
            cursor.execute("SELECT email, password FROM member WHERE email = %s AND password = %s",
                           (email, password))
            result = cursor.fetchone()

            if result:
                return 'Login successful'
            else:
                return 'Invalid email or password'
        except pymysql.Error as e:
            print(f"Database error: {e}")
            con.rollback()
            return 'Database error'
        finally:
            cursor.close()
            con.close()

    def register(self, firstName, lastName, displayName, email, password, address, phone):
        con = self.connect()
        cursor = con.cursor()
        db = Database()

        try:
            # Check if the email already exists in the database
            cursor.execute("SELECT * FROM `member` WHERE `email` = %s", (email,))
            existing_user = cursor.fetchone()

            cursor.execute("SELECT * FROM `member` WHERE `displayName` = %s", (displayName,))
            existing_username = cursor.fetchone()

            if existing_user:
                return 'User with this email already exists'
            if existing_username:
                return 'This username already exists'
            elif firstName and lastName and displayName and email and password and address and phone:
                cursor.execute(
                    "INSERT INTO `member`(`firstName`, `lastName`, `displayName`, `email`, `password`, `address`, `phone`) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (firstName, lastName, displayName, email, password, address, phone)
                )
                con.commit()  # Commit the changes to the database

                # Get the newly created user's memberId
                user_id = db.getUserIdByUsername(username=displayName)

                # Create an initial shopping cart record for the user
                cursor.execute(
                    "INSERT INTO shoppingweb.shoppingcart(price, quantity, memberId, productId) "
                    "VALUES (%s, %s, %s, %s)",
                    (857, 0, user_id, 1)
                )
                con.commit()

                return 'Registration successful'
            else:
                return 'Please provide all necessary information for registration'
        except pymysql.Error as e:
            print(f"Database error: {e}")
            con.rollback()  # Rollback changes in case of error
            return 'Registration failed'
        finally:
            cursor.close()
            con.close()

    def addToShoppingCart(self, username, productId, quantity):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT * FROM shoppingweb.shoppingcart "
                "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s) "
                "AND productId = %s;",
                (username, productId)
            )

            result = cursor.fetchone()  # 获取单行结果
            if result:
                print("存在相同的商品和用户")
                # 这里执行更新购物车数量的操作
                cursor.execute(
                    "UPDATE shoppingweb.shoppingcart SET quantity = quantity + %s "
                    "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s) "
                    "AND productId = %s;",
                    (quantity, username, productId)
                )
                # 提交事务
                con.commit()
            else:
                print("不存在相同的商品和用户")
                # 这里执行插入新记录到购物车的操作
                cursor.execute(
                    "INSERT INTO shoppingweb.shoppingcart (price, quantity, memberId, productId) "
                    "VALUES ("
                    "(SELECT price FROM shoppingweb.product WHERE productId = %s), "
                    "%s, "
                    "(SELECT memberId FROM shoppingweb.member WHERE displayName = %s), "
                    "%s)",
                    (productId, quantity, username, productId)
                )
                # 提交事务
                con.commit()

            # 获取价格并返回
            cursor.execute(
                "SELECT price FROM shoppingweb.product WHERE productId = %s;",
                (productId,)
            )
            price = cursor.fetchone()
            print(price)
            if price:
                return price[0]  # Return the first column value (price)
            else:
                return 0  # Return 0 if no price found for the given productId

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return 0  # Return 0 if there's a database error
        finally:
            cursor.close()
            con.close()

    def deleteUserShoppingCart(self, username, productId):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "DELETE FROM shoppingweb.shoppingcart "
                "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s) "
                "AND productId = %s;",
                (username, productId)
            )

            # 提交事务
            con.commit()

            # 返回删除的产品价格
            cursor.execute(
                "SELECT price FROM shoppingweb.product WHERE productId = %s;",
                (productId,)
            )
            price = cursor.fetchone()
            print(price)
            if price:
                return price[0]  # 返回第一列的值（价格）
            else:
                return 0  # 如果给定productId找不到价格，则返回0

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return 0  # 如果发生数据库错误，则返回0
        finally:
            cursor.close()
            con.close()

    def getUserShoppingCartByUsername(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT * FROM shoppingweb.shoppingcart "
                "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s);",
                (username,)
            )

            shopping_cart = cursor.fetchall()
            return shopping_cart

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None  # Return None if there's a database error
        finally:
            cursor.close()
            con.close()

    def getUserShoppingCartTotalPriceByUsername(self, username):
        con = self.connect()
        db = Database()
        shopping_cart = db.getUserShoppingCartByUsername(username=username)

        # 检查 shopping_cart 是否为可迭代对象（列表或元组）
        if shopping_cart is None:
            return 0  # 如果 shopping_cart 不可迭代，返回默认值（例如，0）

        total_price = sum(item[1] * item[2] for item in shopping_cart)
        return total_price

    def getUserShoppingCartTotalQuantityByUsername(self, username):
        con = self.connect()
        db = Database()
        shopping_cart = db.getUserShoppingCartByUsername(username=username)

        if shopping_cart is None:
            return 0  # 如果 shopping_cart 是 None，返回一个默认值（例如，0）

        total_quantity = sum(item[2] for item in shopping_cart)  # 计算总数量
        return total_quantity

    def addOrderAndDeleteUserShoppingCart(self, firstName, lastName, address, phoneNumber, email, note, username):
        con = self.connect()
        cursor = con.cursor()
        db = Database()
        memberId = db.getUserIdByUsername(username=username)
        try:
            # 插入訂單信息到 ordersheet 表中
            cursor.execute(
                "INSERT INTO ordersheet (firstName, lastName, address, phone, email, note, memberId) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (firstName, lastName, address, phoneNumber, email, note, memberId)
            )
            # 獲取剛插入的 orderId
            orderId = cursor.lastrowid

            # 獲取用戶購物車
            shopping_cart = self.getUserShoppingCartByUsername(username=username)  # 假設 email 就是用戶名稱

            # 將購物車產品信息添加到 ordersheet_has_product 表中
            for item in shopping_cart:
                print(item)
                productId, price, quantity = item[4], item[1], item[2]
                cursor.execute(
                    "INSERT INTO shoppingweb.ordersheet_has_product (orderId, productId, price, quantity) "
                    "VALUES (%s, %s, %s, %s)",
                    (orderId, productId, price, quantity)
                )
            cursor.execute("DELETE FROM shoppingcart WHERE memberId = %s;", memberId)

            con.commit()
            return orderId  # 返回新增訂單的 orderId

        except pymysql.Error as e:
            print(f"Database error: {e}")
            con.rollback()
            return None
        finally:
            cursor.close()
            con.close()

    def getUserOrdersByUsername(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT ordersheet_has_product.orderId, ordersheet_has_product.productId, "
                           "ordersheet_has_product.quantity, ordersheet_has_product.price "
                           "FROM ordersheet_has_product "
                           "INNER JOIN ordersheet ON ordersheet_has_product.orderId = ordersheet.orderId "
                           "INNER JOIN member ON ordersheet.memberId = member.memberId "
                           "WHERE member.displayName = %s;",
                           (username,)
                           )

            orders = cursor.fetchall()
            for order in orders:
                # 在這裡處理每一個找到的訂單
                orderId, productId, quantity, price = order[0], order[1], order[2], order[3]
                # 執行您想要的操作，例如將這些訂單資訊傳遞給模板或進行其他處理
            return orders

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            con.close()

    def getAllProductsName(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT productName FROM shoppingweb.product")
            products = cursor.fetchall()
            return products
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            con.close()

    def getUserOrderTotalPriceByUsername(self, username):
        con = self.connect()
        db = Database()
        shopping_cart = db.getUserOrdersByUsername(username=username)
        totalPrice = sum(item[2] * item[3] for item in shopping_cart)
        return totalPrice

    def getUserInformationByUsername(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM shoppingweb.member WHERE displayName = %s", username)
            memberInformation = cursor.fetchone()
            return memberInformation
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            con.close()

    def editUserInformationByUsername(
            self,
            firstName,
            lastName,
            username,
            displayName,
            email,
            oldPassword,
            newPassword=None,
            confirmNewPassword=None
    ):
        con = self.connect()
        cursor = con.cursor()
        memberId = Database().getUserIdByUsername(username=username)
        try:
            # Check if username exists
            cursor.execute("SELECT * FROM shoppingweb.member WHERE displayName = %s", username)
            memberInformation = cursor.fetchone()
            print(memberInformation)
            if memberInformation:
                # Check if the old password matches
                if oldPassword != memberInformation[5]:
                    return False  # Return False if the old password does not match

                if newPassword is not None and confirmNewPassword is not None and newPassword != '' and confirmNewPassword != '':
                    # Update member information (including password change if applicable)
                    if newPassword == confirmNewPassword:
                        cursor.execute("UPDATE shoppingweb.member SET firstName = %s, lastName = %s, displayName = %s, email = %s, password = %s "
                                       "WHERE displayName = %s AND memberId = %s",
                                       (firstName, lastName, displayName, email, newPassword, username, memberId))
                        con.commit()
                        return True  # Return True if information is updated successfully
                    else:
                        return False  # Return False if new password and confirm password do not match
                else:
                    # Update member information excluding password change
                    cursor.execute("UPDATE shoppingweb.member SET firstName = %s, lastName = %s, displayName = %s, email = %s, password = %s "
                                   "WHERE displayName = %s AND memberId = %s",
                                   (firstName, lastName, displayName, email, oldPassword, username, memberId))
                    con.commit()
                    return True  # Return True if information is updated successfully (without password change)
            return False  # Return False if member with given username does not exist

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            con.close()

    def checkUserShoppingIsEmpty(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM shoppingweb.shoppingcart "
                           "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s)", "test")
            result = cursor.fetchone()
            if result is None:
                return True
            else:
                return False
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            con.close()
