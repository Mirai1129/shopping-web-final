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

    def getUsername(self, email):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT displayName FROM shoppingweb.member WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def shoppingCartQuantity(self, username):
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

    def shoppingCartPrice(self, username):
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

        try:
            # Check if the email already exists in the database
            cursor.execute("SELECT * FROM `member` WHERE `email` = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                return 'User with this email already exists'
            elif firstName and lastName and displayName and email and password and address and phone:
                cursor.execute(
                    "INSERT INTO `member`(`firstName`, `lastName`, `displayName`, `email`, `password`, `address`, `phone`) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (firstName, lastName, displayName, email, password, address, phone)
                )
                con.commit()  # Commit the changes to the database
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
            print("cursor.fetchone()", result)
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

    def getUserShoppingCart(self, username):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT * FROM shoppingweb.shoppingcart "
                "WHERE memberId = (SELECT memberId FROM shoppingweb.member WHERE displayName = %s);",
                (username,)
            )

            shopping_cart = cursor.fetchall()
            print(shopping_cart)
            return shopping_cart

        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None  # Return None if there's a database error
        finally:
            cursor.close()
            con.close()

    def getUserShoppingCartTotalPrice(self, username):
        con = self.connect()
        db = Database()
        shopping_cart = db.getUserShoppingCart(username=username)
        total_price = sum(item[1] * item[2] for item in shopping_cart)
        return total_price

    def getUserShoppingCartTotalQuantity(self, username):
        con = self.connect()
        db = Database()
        shopping_cart = db.getUserShoppingCart(username=username)
        total_quantity = sum(item[2] for item in shopping_cart)  # Calculate total quantity
        return total_quantity
