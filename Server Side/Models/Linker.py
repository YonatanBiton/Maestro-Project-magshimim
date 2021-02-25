import mysql.connecter

DB_HOST = "localhost"
DB_USER = "maestro"
DB_PASSWORD = "test"
DB_NAME = "maestro"

class Linker:
    def __init__(self):
        self.db = mysql.connector.connect (
            host = DB_HOST,
            user = DB_USER,
            password = DB_PASSWORD,
            database = DB_NAME
        )
        self.cursor = db.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
        (id INT AUTO_INCREMENT, user_name VARCHAR(20) NOT NULL, password VARCHAR(30) NOT NULL, email VARCHAR(254) NOT NULL, PRIMARY KEY (id));""")