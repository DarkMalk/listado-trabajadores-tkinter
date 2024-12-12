from models import Database
from .user_info import UserInfo
from .user_info_work import UserInfoWork
import bcrypt

class User(UserInfo, UserInfoWork):
    def __init__(
        self,
        username=None,
        password=None,
        email=None,
        role=None,
        name=None,
        lastname=None,
        rut=None,
        gender=None,
        direction=None,
        phone=None,
        entry_date=None,
        department=None,
        area=None,
        job_title=None
    ):
        UserInfo.__init__(self, name, lastname, rut, gender, direction, phone)
        UserInfoWork.__init__(self, entry_date, department, area, job_title)
        self.username = username
        self.password = password
        self.email = email
        self.role = role


    def update(
        self,
        id,
        username=None,
        email=None,
        role=None,
    ):
        try:
            db = Database()
            sql = "UPDATE user SET username = %s, email = %s, role = %s WHERE id = %s"
            db.execute(sql, (username, email, role, id))
        except Exception as e:
            print(e)

    def save(self):
        try:
            db = Database()
            sql = "INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)"
            password_encrypt = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt(10))
            db.execute(sql, (self.username, password_encrypt, self.email, self.role))
            
            id_user = self.get_id_user(self.username)["id"]

            self.save_info(id_user)
            self.save_info_work(id_user)
        except Exception as e:
            print(e)

    def login(self, username, password):
        try:
            db = Database()
            sql = "SELECT username, password FROM user WHERE username = %s"
            result = db.query_one(sql, [username])

            return bcrypt.checkpw(password.encode("utf-8"), result["password"].encode("utf-8"))
        except Exception as e:
            print(e)

    def get_all(self):
        try:
            db = Database()
            sql = "SELECT u.id, u.username, u.email, r.name as role, ui.name, ui.lastname, ui.rut, g.name as gender, ui.direction, ui.phone, uiw.entry_date, de.name as department, ar.name as area, jt.name as job_title FROM user u INNER JOIN role r ON r.id = u.role LEFT JOIN user_info ui ON ui.id_user = u.id LEFT JOIN gender g ON ui.gender = g.id LEFT JOIN user_info_work uiw ON uiw.id_user = u.id LEFT JOIN department de ON de.id = uiw.department LEFT JOIN area ar ON ar.id = uiw.area LEFT JOIN job_title jt ON jt.id = uiw.job_title"
            return db.query(sql)
        except Exception as e:
            print(e)

    def get_id_user(self, username):
        try:
            db = Database()
            sql = "SELECT id FROM user WHERE username = %s"
            return db.query_one(sql, [username])
        except Exception as e:
            print(e)

    def get_user(self, id):
        try:
            db = Database()
            sql = "SELECT u.id, u.username, u.email, r.name as role, ui.name, ui.lastname, ui.rut, g.name as gender, ui.direction, ui.phone, uiw.entry_date, de.name as department, ar.name as area, jt.name as job_title FROM user u INNER JOIN role r ON r.id = u.role LEFT JOIN user_info ui ON ui.id_user = u.id LEFT JOIN gender g ON ui.gender = g.id LEFT JOIN user_info_work uiw ON uiw.id_user = u.id LEFT JOIN department de ON de.id = uiw.department LEFT JOIN area ar ON ar.id = uiw.area LEFT JOIN job_title jt ON jt.id = uiw.job_title WHERE u.id = %s"
            return db.query_one(sql, [id])
        except Exception as e:
            print(e)


    def delete(self, id):
        try:
            db = Database()
            sql = "DELETE FROM user WHERE id = %s"
            db.execute(sql, [id])
        except Exception as e:
            print(e)