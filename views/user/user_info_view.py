from tkinter import Tk, LabelFrame as LabelFrameTk
from tkinter.ttk import Label, Labelframe, Button

class UserInfoView(Tk):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.frame1 = LabelFrameTk(self, bd=0, relief="flat")
        self.frame1.grid(row=0, column=0, padx=24, pady=12)

        self.frame2 = LabelFrameTk(self, bd=0, relief="flat")
        self.frame2.grid(row=0, column=1, padx=24, pady=12)

        self.btn_close = Button(self, text="Close", command=self.destroy)
        self.btn_close.grid(row=1, column=0, columnspan=2, padx=24, pady=12)

        self.widgets_user(self.frame1)
        self.widgets_user_info(self.frame2)
        self.widgets_user_info_work(self.frame1)
        self.config()

        self.mainloop()

    def widgets_user(self, frame):
        label_frame = Labelframe(frame, text="User: ")
        label_frame.grid(row=0, column=0, pady=(0, 12))

        Label(label_frame, text=f"Username: {self.user["username"]}").grid(row=0, column=0, padx=12, pady=(12, 0))

        Label(label_frame, text=f"Email: {self.user["email"]}").grid(row=1, column=0, padx=12, pady=(12, 0))

        Label(label_frame, text=f"Role: {self.user["role"]}").grid(row=2, column=0, padx=12, pady=12)

    def widgets_user_info(self, frame):
        label_frame = Labelframe(frame, text="User Info: ")
        label_frame.grid(row=0, column=1, padx=(12, 24), pady=12)
        Label(label_frame, text=f"Name: {self.user["name"]}").grid(row=0, column=0)

        Label(label_frame, text=f"Lastname: {self.user["lastname"]}").grid(row=1, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Rut: {self.user["rut"]}").grid(row=2, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Gender: {self.user["gender"]}").grid(row=3, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Direction: {self.user["direction"]}").grid(row=4, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Phone: {self.user["phone"]}").grid(row=5, column=0, padx=24, pady=12)

    def widgets_user_info_work(self, frame):
        label_frame = Labelframe(frame, text="User Info Work: ")
        label_frame.grid(row=1, column=0)

        Label(label_frame, text=f"Entry Date: {self.user["entry_date"]}").grid(row=0, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Department: {self.user["department"]}").grid(row=1, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Area: {self.user["area"]}").grid(row=2, column=0, padx=24, pady=12)

        Label(label_frame, text=f"Job Title: {self.user["job_title"]}").grid(row=3, column=0, padx=24, pady=12)

    def config(self):
        self.title("User Info")
        self.resizable(False, False)