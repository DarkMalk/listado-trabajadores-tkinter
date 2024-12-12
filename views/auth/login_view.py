from tkinter import messagebox, Tk
from tkinter.ttk import Label, Button, Entry
from models import User
from ..home import HomeView

class LoginView(Tk):
    def __init__(self):
        super().__init__()

        self.widgets()
        self.config()

        # Run the main loop
        self.mainloop()

    def widgets(self):
        Label(self, text="Username").grid(row=0, column=0, padx=24, columnspan=2, pady=(16, 0))
        self.input_username = Entry(self)
        self.input_username.grid(row=1, column=0, columnspan=4, padx=24)

        Label(self, text="Password").grid(row=2, column=0, columnspan=2, padx=24)
        self.input_password = Entry(self, show="*")
        self.input_password.grid(row=3, column=0, columnspan=4, padx=24)

        self.btn_login = Button(self, text="Login", command=self.login)
        self.btn_login.grid(row=4, column=0, columnspan=4, padx=24, pady=(0, 16))

    def login(self):
        username = self.input_username.get()
        password = self.input_password.get()

        if User().login(username, password):
            self.destroy()
            my_user_id = User().get_id_user(username)["id"]
            HomeView(my_user_id)
        else:
            messagebox.showerror("Login failed", "Invalid username or password")

    def config(self):
        self.title("Login")
        self.resizable(False, False)