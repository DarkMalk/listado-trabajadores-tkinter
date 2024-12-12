import mysql.connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            database=getenv("DB_NAME")
        )
    
    def query(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()

    def execute(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()

    def query_one(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()