from models import Database

class JobTitle:
    def __init__(self, name = None):
        self.name = name
    
    def save(self):
        try:
            db = Database()
            sql = "INSERT INTO job_title (name) VALUES (%s)"
            db.execute(sql, [self.name])
        except Exception as e:
            print(e)

    def get_all(self):
        try:
            db = Database()
            sql = "SELECT * FROM job_title"
            return db.query(sql)
        except Exception as e:
            print(e)