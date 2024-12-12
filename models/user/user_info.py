from models import Database

class UserInfo:
    def __init__(self, name = None, lastname = None, rut = None, gender = None, direction = None, phone = None):
       self.name = name
       self.lastname = lastname
       self.rut = rut
       self.gender = gender
       self.direction = direction
       self.phone = phone

    def save_info(self, id_user):
        try:
            db = Database()
            sql = "INSERT INTO user_info (name, lastname, rut, gender, direction, phone, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            db.execute(sql, (self.name, self.lastname, self.rut, self.gender, self.direction, self.phone, id_user))
        except Exception as e:
            print(e)

    def update_info(self, id_user, new_name, new_lastname, new_rut, new_gender, new_direction, new_phone):
        try:
            db = Database()
            
            sql_search = "SELECT id FROM user_info WHERE id_user = %s"
            result = db.query_one(sql_search, [id_user])

            if not result:
                self.name = new_name
                self.lastname = new_lastname
                self.rut = new_rut
                self.gender = new_gender
                self.direction = new_direction
                self.phone = new_phone
                self.save_info(id_user)
                return
            
            sql = "UPDATE user_info SET name = %s, lastname = %s, rut = %s, gender = %s, direction = %s, phone = %s WHERE id_user = %s"
            db.execute(sql, (new_name, new_lastname, new_rut, new_gender, new_direction, new_phone, id_user))


        except Exception as e:
            print(e)