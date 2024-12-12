from models import Database

class UserInfoWork:
    def __init__(self, entry_date = None, department = None, area = None, job_title = None):
        self.entry_date = entry_date
        self.department = department
        self.area = area
        self.job_title = job_title

    def save_info_work(self, id_user):
        try:
            db = Database()
            sql = "INSERT INTO user_info_work (id_user, entry_date, department, area, job_title) VALUES (%s, %s, %s, %s, %s)"
            db.execute(sql, (id_user, self.entry_date, self.department, self.area, self.job_title))
        except Exception as e:
            print(e)

    def update_info_work(self, id_user, new_entry_date, new_department, new_area, new_job_title):
        try:
            db = Database()

            sql_search = "SELECT id FROM user_info_work WHERE id_user = %s"
            result = db.query_one(sql_search, [id_user])

            if not result:
                self.entry_date = new_entry_date
                self.department = new_department
                self.area = new_area
                self.job_title = new_job_title
                self.save_info_work(id_user)
                return

            sql = "UPDATE user_info_work SET entry_date = %s, department = %s, area = %s, job_title = %s WHERE id_user = %s"
            db.execute(sql, (new_entry_date, new_department, new_area, new_job_title, id_user))
        except Exception as e:
            print(e)

    def delete(self, id_user):
        try:
            db = Database()
            sql = "DELETE FROM user_info_work WHERE id_user = %s"
            db.execute(sql, [id_user])
        except Exception as e:
            print(e)