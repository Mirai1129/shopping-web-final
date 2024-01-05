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
