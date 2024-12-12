from tkinter import Tk, Listbox, END
from tkinter.ttk import Button, Label
from utils.modules import MODULES
from .user import UserInfoView, UsersView, CreateOrUpdateUserView
from .family_responsabilities import ManageFamilyResponsabilitiesView
from .emergency_contact import ManageEmergencyContactView
from models import User

class HomeView(Tk):
    list_modules = []

    def __init__(self, user_id):
        super().__init__()
        self.my_user = User().get_user(user_id)

        self.widgets()
        self.config()
        self.set_modules(MODULES.get(self.my_user["role"]))

        # Start the main loop
        self.mainloop()

    def widgets(self):
        self.label_auth = Label(self, text=f"Welcome {self.my_user['username']}")
        self.label_auth.grid(row=0, column=0, padx=24, pady=(12, 0))

        self.list_box = Listbox(self)
        self.list_box.grid(row=1, column=0, padx=24, pady=12)

        self.btn_close = Button(self, text="Close", command=self.close)
        self.btn_close.grid(row=2, column=0, padx=24, pady=(0, 12))


    def config(self):
        self.title("List Modules")
        self.resizable(False, False)

    def set_modules(self, data):
        self.list_modules = data
        self.list_box.delete(0, END)

        for module in self.list_modules:
            self.list_box.insert(END, module)

        self.list_box.bind("<Double-Button-1>", self.open_module)
    
    def open_module(self, event):
        index = self.list_box.curselection()[0]
        module = self.list_modules[index]

        if module == "List Users":
            UsersView()
        elif module == "Create User":
            CreateOrUpdateUserView()
        elif module == "Update My Profile":
            CreateOrUpdateUserView(self.my_user, my_profile=True)
        elif module == "View My Profile":
            UserInfoView(self.my_user)
        elif module == "Manage My Family Responsabilities":
            ManageFamilyResponsabilitiesView(self.my_user)
        elif module == "Manage My Emergency Contact":
            ManageEmergencyContactView(self.my_user)


    def close(self):
        self.destroy()