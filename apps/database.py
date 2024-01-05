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
