from models import Database

class Gender:
    def __init__(self, name = None):
        self.name = name
    
    def save(self):
        try:
            db = Database()
            sql = "INSERT INTO gender (name) VALUES (%s)"
            db.execute(sql, [self.name])
        except Exception as e:
            print(e)

    def get_all(self):
        try:
            db = Database()
            sql = "SELECT * FROM gender"
            return db.query(sql)
        except Exception as e:
            print(e)