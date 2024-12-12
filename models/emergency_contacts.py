from .database import Database

class EmergencyContact:
    def __init__(self, name = None, relationship = None, phone = None):
        self.name = name
        self.relationship = relationship
        self.phone = phone
    
    def save(self, id_user):
        try:
            db = Database()
            sql = "INSERT INTO user_emergency_contact (id_user, name, relationship, phone) VALUES (%s, %s, %s, %s)"
            db.execute(sql, [id_user, self.name, self.relationship, self.phone])
        except Exception as e:
            print(e)

    def get_all(self, id_user):
        try:
            db = Database()
            sql = "SELECT ec.id, ec.name, ec.phone, r.name as relationship FROM user_emergency_contact ec LEFT JOIN relationship r ON r.id = ec.relationship WHERE ec.id_user = %s"
            return db.query(sql, [id_user])
        except Exception as e:
            print(e)

    def update(self, id, name, relationship, phone):
        try:
            db = Database()
            sql = "UPDATE user_emergency_contact SET name = %s, relationship = %s, phone = %s WHERE id = %s"
            db.execute(sql, [name, relationship, phone, id])
        except Exception as e:
            print(e)

    def delete(self, id):
        try:
            db = Database()
            sql = "DELETE FROM user_emergency_contact WHERE id = %s"
            db.execute(sql, [id])
        except Exception as e:
            print(e)