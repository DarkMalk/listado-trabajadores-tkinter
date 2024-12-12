from tkinter import Tk, messagebox
from tkinter.ttk import Combobox, Entry, Button, Label, Labelframe
from models import Gender, Department, Area, Role, JobTitle, User
from datetime import datetime
import re

class CreateOrUpdateUserView(Tk):
    def __init__(self, user=None, on_close_callback=None, my_profile=False):
        super().__init__()
        self.user = user
        self.on_close_callback = on_close_callback
        self.is_my_profile = my_profile

        self.gender_list = Gender().get_all()
        self.department_list = Department().get_all()
        self.role_list = Role().get_all()
        self.area_list = Area().get_all()
        self.job_title_list = JobTitle().get_all()

        frame_left = Labelframe(self, text="User Data")
        frame_left.grid(row=0, column=0, padx=12, pady=12)

        frame_right = Labelframe(self, text="User Selections")
        frame_right.grid(row=0, column=1, padx=12, pady=12)

        self.btn_save = Button(self, text="Save", command=self.save)
        self.btn_save.grid(row=1, column=0, columnspan=2, pady=12)

        self.widgets_user(frame_left)
        self.widgets_selections(frame_right)

        self.fill_user()
        self.lock_inputs()
        self.config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def widgets_selections(self, frame):
        Label(frame, text="Role").grid(row=0, column=0)
        self.box_role = Combobox(frame, values=[role["name"] for role in self.role_list], state="readonly")
        self.box_role.grid(row=0, column=1)

        Label(frame, text="Gender").grid(row=1, column=0)
        self.box_gender = Combobox(frame, values=[gender["name"] for gender in self.gender_list], state="readonly")
        self.box_gender.grid(row=1, column=1)

        Label(frame, text="Area").grid(row=2, column=0)
        self.box_area = Combobox(frame, values=[area["name"] for area in self.area_list], state="readonly")
        self.box_area.grid(row=2, column=1)

        Label(frame, text="Department").grid(row=3, column=0)
        self.box_department = Combobox(frame, values=[department["name"] for department in self.department_list], state="readonly")
        self.box_department.grid(row=3, column=1)

        Label(frame, text="Job Title").grid(row=4, column=0)
        self.box_job_title = Combobox(frame, values=[job_title["name"] for job_title in self.job_title_list], state="readonly")
        self.box_job_title.grid(row=4, column=1)
    
    def widgets_user(self, frame):
        Label(frame, text="Username").grid(row=0, column=0)
        self.input_username = Entry(frame)
        self.input_username.grid(row=0, column=1)

        Label(frame, text="Password").grid(row=1, column=0)
        self.input_password = Entry(frame, show="*")
        self.input_password.grid(row=1, column=1)

        Label(frame, text="Email").grid(row=2, column=0)
        self.input_email = Entry(frame)
        self.input_email.grid(row=2, column=1)

        Label(frame, text="Name").grid(row=3, column=0)
        self.input_name = Entry(frame)
        self.input_name.grid(row=3, column=1)

        Label(frame, text="Lastname").grid(row=4, column=0)
        self.input_lastname = Entry(frame)
        self.input_lastname.grid(row=4, column=1)

        Label(frame, text="Rut").grid(row=5, column=0)
        self.input_rut = Entry(frame)
        self.input_rut.grid(row=5, column=1)

        Label(frame, text="Direction").grid(row=6, column=0)
        self.input_direction = Entry(frame)
        self.input_direction.grid(row=6, column=1)

        Label(frame, text="Phone").grid(row=7, column=0)
        self.input_phone = Entry(frame)
        self.input_phone.grid(row=7, column=1)

        Label(frame, text="Entry Date").grid(row=8, column=0)
        self.input_entry_date = Entry(frame)
        self.input_entry_date.grid(row=8, column=1)

    def save(self):
        username = self.input_username.get()
        password = self.input_password.get()
        email = self.input_email.get()
        name = self.input_name.get()
        lastname = self.input_lastname.get()
        rut = self.input_rut.get()
        direction = self.input_direction.get()
        phone = self.input_phone.get()
        role = self.option_selected(self.role_list, self.box_role)["id"] if self.box_role.get() else None
        gender = self.option_selected(self.gender_list, self.box_gender)["id"] if self.box_gender.get() else None
        area = self.option_selected(self.area_list, self.box_area)["id"] if self.box_area.get() else None
        department = self.option_selected(self.department_list, self.box_department)["id"] if self.box_department.get() else None
        job_title = self.option_selected(self.job_title_list, self.box_job_title)["id"] if self.box_job_title.get() else None
        entry_date = self.input_entry_date.get()

        if not self.validate("update" if self.user else "create", username=username, password=password, email=email, name=name, lastname=lastname, rut=rut, direction=direction, phone=phone, role=role, gender=gender, area=area, department=department, job_title=job_title, entry_date=entry_date):
            return
        
        if self.user:
            User().update(self.user["id"], username, email, role)
            User().update_info(self.user["id"], name, lastname, rut, gender, direction, phone)
            User().update_info_work(self.user["id"], entry_date, department, area, job_title)
            messagebox.showinfo("Success", "User updated successfully")
        else:
            User(username, password, email, role, name, lastname, rut, gender, direction, phone, entry_date, department, area, job_title).save()
            messagebox.showinfo("Success", "User created successfully")

    def validate(self, mode="create", **kwargs):
        required_fields = ['username', 'password', 'email', 'name', 'lastname', 'rut', 'direction', 'phone', 'entry_date']
        selection_fields = ['role', 'gender', 'area', 'department', 'job_title']

        REGEX_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        REGEX_RUT = r"^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$"
        PHONE_REGEX = r'^[2-9] \d{3,4} \d{4}$'
        ENTRY_DATE_REGEX = r'^\d{4}-\d{2}-\d{2}$'


        if mode == "update":
            required_fields.remove('password')

        for field in required_fields:
            if not kwargs.get(field):
                messagebox.showerror("Error", f"The field '{field}' is required")
                return False

        for field in selection_fields:
            if not kwargs.get(field):
                messagebox.showerror("Error", f"The selection '{field}' is required")
                return False
            
        if not re.match(REGEX_EMAIL, kwargs.get('email')):
            messagebox.showerror("Error", "Invalid email format (ex: user@example.com)")
            return False
        
        if not re.match(REGEX_RUT, kwargs.get('rut')):
            messagebox.showerror("Error", "Invalid RUT format (ex: 12.345.678-9)")
            return False
        
        if not re.match(PHONE_REGEX, kwargs.get('phone')):
            messagebox.showerror("Error", "Invalid phone format (ex: 9 1234 5678 or 2 1234 5678)")
            return False
        
        if not re.match(ENTRY_DATE_REGEX, kwargs.get('entry_date')):
            messagebox.showerror("Error", "Invalid entry date format (ex: 2021-12-31)")
            return False

        try:
            datetime.strptime(kwargs.get('entry_date'), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Check the entry date (ex: 2021-12-31)")
            return False

        return True


    def option_selected(self, list, box):
        selected_name = box.get()
        return next((item for item in list if item["name"] == selected_name), None)
        

    def config(self):
        if self.user:
            self.title("Update User")
        else:
            self.title("Create User")
        
        self.resizable(False, False)

    def fill_user(self):
        if not self.user:
            return
        
        self.input_username.insert(0, self.user["username"] if self.user["username"] else "")
        self.input_password.configure(state="disabled")
        self.input_email.insert(0, self.user["email"] if self.user["email"] else "")
        self.input_name.insert(0, self.user["name"] if self.user["name"] else "")
        self.input_lastname.insert(0, self.user["lastname"] if self.user["lastname"] else "")
        self.input_rut.insert(0, self.user["rut"] if self.user["rut"] else "")
        self.input_direction.insert(0, self.user["direction"] if self.user["direction"] else "")
        self.input_phone.insert(0, self.user["phone"] if self.user["phone"] else "")

        self.box_role.set(self.user["role"] if self.user["role"] else "")
        self.box_gender.set(self.user["gender"] if self.user["gender"] else "")
        self.box_area.set(self.user["area"] if self.user["area"] else "")
        self.box_department.set(self.user["department"] if self.user["department"] else "")
        self.box_job_title.set(self.user["job_title"] if self.user["job_title"] else "")
        self.input_entry_date.insert(0, self.user["entry_date"] if self.user["entry_date"] else "")
    
    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        
        self.destroy()

    def lock_inputs(self):
        if not self.is_my_profile:
            return
        
        # Inputs
        self.input_username.configure(state="disabled")
        self.input_name.configure(state="disabled")
        self.input_lastname.configure(state="disabled")
        self.input_rut.configure(state="disabled")
        self.input_entry_date.configure(state="disabled")

        # Selections
        self.box_role.configure(state="disabled")
        self.box_gender.configure(state="disabled")
        self.box_department.configure(state="disabled")
        self.box_area.configure(state="disabled")
        self.box_job_title.configure(state="disabled")
