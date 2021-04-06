import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "maestro_db"

class Linker:
    def __init__(self):
        try:
            self.__db = mysql.connector.connect (
                host = DB_HOST,
                user = DB_USER,
                password = DB_PASSWORD,
                database = DB_NAME
            )
            self.__cursor = self.__db.cursor()

            self.__cursor.execute("CREATE TABLE IF NOT EXISTS users "
            "(id INT AUTO_INCREMENT, active INT NOT NULL, name VARCHAR(20) NOT NULL UNIQUE,"
            " password VARCHAR(30) NOT NULL, email VARCHAR(254) NOT NULL UNIQUE, PRIMARY KEY (id));")
        except mysql.connector.Error as mysql_error:
            print (f"Failed to open the database!!!\nSQL Error: {str(mysql_error)}")
        except Exception as ex:
            print (f"Failed to open the database!!!\nPython Error: {str(ex)}")
    

    def login_user(self, user_name, password):
        db_result = self.query("SELECT password FROM users WHERE name=%(user_name)s;",
        {'user_name' : user_name}, f"Failed to query login on user - {user_name}")
        if db_result == None or len(db_result) == 0 or len(db_result[0]) == 0:
            return False
        if db_result[0][0] == password:
            return True
        return False


    def register_user(self, user_name, password, email):
        rows_affected = self.non_query("INSERT INTO users (name, active, password, email) "
        "VALUES (\'%(user_name)s\', 1, \'%(password)s\', \'%(email)s\');",
        {'user_name': user_name, 'password': password, 'email' : email}, f"Failed to query register on user - {user_name}")
        if rows_affected == None:
            return False
        return True


    def query(self, message, args={}, error_message="Db query error!"):
        if self.non_query(message, args, error_message) == None:
            return None
        return self.__cursor.fetchall()


    def non_query(self, message, args={}, error_message="Db query error!"):
        try:
            query = message % args
            print(f'SQL Quary: {query}')
            self.__cursor.execute(query)
            self.__db.commit()
            print(self.__cursor.rowcount)
            return self.__cursor.rowcount if self.__cursor.rowcount > 0 else None
        except mysql.connector.Error as mysql_error:
            print (f"{error_message}\nSQL Error: {str(mysql_error)}")
            return None
        except Exception as ex:
            print (f"{error_message}\nPython Error: {str(ex)}")
            return None