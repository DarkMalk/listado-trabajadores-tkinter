from tkinter import Tk, END, messagebox, Button
from tkinter.ttk import Treeview, Button, Labelframe, Entry
from models import User
from .user_info_view import UserInfoView
from .create_or_update_user import CreateOrUpdateUserView
from ..family_responsabilities import ManageFamilyResponsabilitiesView
from ..emergency_contact import ManageEmergencyContactView


class UsersView(Tk):
    list_users = []

    def __init__(self):
        super().__init__()

        self.widgets()
        self.set_users()
        self.widgets_options()

        # Config
        self.config()
        self.mainloop()

    def widgets(self):
        self.treeview = Treeview(self, columns=("Username", "Name", "Rut", "Email", "Role", "Gender"), show="headings")
        self.treeview.grid(row=0, column=0, columnspan=4, padx=24, pady=(24, 12))

        self.treeview.heading("Username", text="Username")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Rut", text="Rut")
        self.treeview.heading("Email", text="Email")
        self.treeview.heading("Role", text="Role")
        self.treeview.heading("Gender", text="Gender")

        self.treeview.column("Username", width=150, anchor="center")
        self.treeview.column("Name", width=150, anchor="center")
        self.treeview.column("Rut", width=150, anchor="center")
        self.treeview.column("Email", width=150, anchor="center")
        self.treeview.column("Role", width=150, anchor="center")
        self.treeview.column("Gender", width=150, anchor="center")

        self.treeview.grid_columnconfigure(0, weight=1)
        self.treeview.grid_columnconfigure(1, weight=1)
        self.treeview.grid_columnconfigure(2, weight=1)
        self.treeview.grid_columnconfigure(3, weight=1)
        self.treeview.grid_columnconfigure(4, weight=1)
        self.treeview.grid_columnconfigure(5, weight=1)

    def widgets_options(self):
        label_frame = Labelframe(self, text="Options")
        label_frame.grid(row=1, column=0, columnspan=4, padx=24, pady=(0, 12))

        self.btn_new = Button(label_frame, text="New User", command=self.open_new_user)
        self.btn_new.grid(row=0, column=0, padx=12, pady=(4, 12))

        self.btn_delete = Button(label_frame, text="Delete User", command=self.delete_user)
        self.btn_delete.grid(row=0, column=1, padx=12, pady=(4, 12))

        self.btn_update = Button(label_frame, text="Update User", command=self.update_user)
        self.btn_update.grid(row=0, column=2, padx=12, pady=(4, 12))

        self.btn_view_info = Button(label_frame, text="View Info", command=self.view_info)
        self.btn_view_info.grid(row=0, column=3, padx=12, pady=(4, 12))
        
        self.btn_manage_emergency_contacts = Button(label_frame, text="Manage Emergency Contacts", command=self.manage_emergency_contacts)
        self.btn_manage_emergency_contacts.grid(row=1, column=0, columnspan=2, padx=12, pady=(4, 12))

        self.btn_manage_family_responsabilities = Button(label_frame, text="Manage Family Responsabilities", command=self.manage_family_responsabilities)
        self.btn_manage_family_responsabilities.grid(row=1, column=2, columnspan=2, padx=12, pady=(4, 12))

    def manage_emergency_contacts(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showerror("Error", "Select a user")
            return
        
        user = self.list_users[index]
        ManageEmergencyContactView(user)

    def manage_family_responsabilities(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showerror("Error", "Select a user")
            return
        
        user = self.list_users[index]
        ManageFamilyResponsabilitiesView(user, self.set_users)

    def open_new_user(self):
        CreateOrUpdateUserView(on_close_callback=self.set_users)

    def delete_user(self):
        index = self.select_item()
        if index == -1 or index is None:
            messagebox.showwarning("Error", "Select a user")
            return
        
        user = self.list_users[index]

        confirm = messagebox.askyesno("Delete User", f"Are you sure you want to delete the user {user['username']}?")

        if confirm:
            User().delete(user["id"])

    def update_user(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showwarning("Error", "Select a user")
            return
        
        user = self.list_users[index]
        CreateOrUpdateUserView(user, self.set_users)

    def on_window_close(self):
        self.destroy()
        self.set_users()

    def view_info(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showerror("Error", "Select a user")
            return
        
        user = self.list_users[index]
        UserInfoView(user)

    def select_item(self):
        selected_item = self.treeview.selection()
        if selected_item:
            selected_id = selected_item[0]
            selected_values = self.treeview.item(selected_id, "values")

            return self.get_user_index(selected_values)

    def get_user_index(self, values):
        for index, user in enumerate(self.list_users):
            if user["username"] == values[0]:
                return index
            
        return -1

    def set_users(self):
        users = User().get_all()

        self.list_users = users
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for user in self.list_users:
            self.treeview.insert("", END, values=(user["username"], user["name"], user["rut"], user["email"], user["role"], user["gender"]))

    def config(self):
        self.title("Users List")
        self.resizable(False, False)