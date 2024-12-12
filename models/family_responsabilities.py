from .database import Database

class FamilyResponsabilities:
    def __init__(self, name = None, rut = None, relationship = None, gender = None):
        self.name = name
        self.rut = rut
        self.relationship = relationship
        self.gender = gender

    def save(self, id_user):
        try:
            db = Database()
            sql = "INSERT INTO family_responsibilities (id_user, name, rut, relationship, gender) VALUES (%s, %s, %s, %s, %s)"
            db.execute(sql, [id_user, self.name, self.rut, self.relationship, self.gender])
        except Exception as e:
            print(e)

    def get_all(self, id_user):
        try:
            db = Database()
            sql = "SELECT fr.id, fr.name, fr.rut, r.name as relationship, g.name as gender FROM family_responsibilities fr LEFT JOIN relationship r ON fr.relationship = r.id LEFT JOIN gender g ON g.id = fr.gender WHERE fr.id_user = %s"
            return db.query(sql, [id_user])
        except Exception as e:
            print(e)

    def update(self, id, new_name, new_rut, new_relationship, new_gender):
        try:
            db = Database()
            sql = "UPDATE family_responsibilities SET name = %s, rut = %s, relationship = %s, gender = %s WHERE id = %s"
            db.execute(sql, [new_name, new_rut, new_relationship, new_gender, id])
        except Exception as e:
            print(e)

    def delete(self, id):
        try:
            db = Database()
            sql = "DELETE FROM family_responsibilities WHERE id = %s"
            db.execute(sql, [id])
        except Exception as e:
            print(e)