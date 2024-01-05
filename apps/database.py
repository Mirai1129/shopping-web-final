import random

import pymysql


class Database:
    def connect(self):
        return pymysql.connect(
            host="localhost",
            user="Mirai1129",
            password="iamdowdwind1129",
            database="shoppingweb",
            charset='utf8mb4'
        )

    def read(self, memberId=0):
        con = self.connect()
        cursor = con.cursor()

        try:
            if memberId == 0:
                cursor.execute("SELECT quantity FROM shoppingcart")
            else:
                cursor.execute("SELECT * FROM phone_book WHERE id = %s ORDER BY name ASC", (memberId,))

            return cursor.fetchone()[0]
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return ()
        finally:
            cursor.close()
            con.close()

    def register(self, firstName, lastName, displayName, email, password, address, phone):
        con = self.connect()
        cursor = con.cursor()
        memberId = random.randint(1000000, 9999999)

        try:
            if firstName and lastName and displayName and email and password and address and phone:
                cursor.execute(
                    "INSERT INTO `member`(`memberId`, `firstName`, `lastName`, `displayName`, `email`, `password`, `address`, `phone`) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (memberId, firstName, lastName, displayName, email, password, address, phone)
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

