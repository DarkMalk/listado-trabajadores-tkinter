from .database import Database


class Relationships:
    def __init__(self, name = None):
        self.name = name 

    def save(self):
        try:
            db = Database()
            sql = "INSERT INTO relationship (name) VALUES (%s)"
            db.execute(sql, [self.name])
        except Exception as e:
            print(e)

    def get_all(self):
        try:
            db = Database()
            sql = "SELECT * FROM relationship"
            return db.query(sql)
        except Exception as e:
            print(e)