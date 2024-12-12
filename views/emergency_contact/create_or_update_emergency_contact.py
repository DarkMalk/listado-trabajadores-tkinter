from tkinter import Tk, messagebox
from tkinter.ttk import Entry, Label, Button, Combobox
from models import Relationships, EmergencyContact
import re

class CreateOrUpdateEmergencyContactView(Tk):
    list_relationships = []
    def __init__(self, user, emergency_contact = None, on_close_callback = None):
        super().__init__()
        self.user = user
        self.emergency_contact = emergency_contact
        self.on_close_callback = on_close_callback

        self.list_relationships = Relationships().get_all()

        self.widgets()
        self.set_data_in_inputs()
        self.config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def widgets(self):
        Label(self, text="Name").grid(row=0, column=0, padx=12, pady=(12, 0))
        self.entry_name = Entry(self)
        self.entry_name.grid(row=0, column=1, padx=12, pady=(12, 0))

        Label(self, text="Phone").grid(row=1, column=0, padx=12, pady=(12, 0))
        self.entry_phone = Entry(self)
        self.entry_phone.grid(row=1, column=1, padx=12, pady=(12, 0))

        Label(self, text="Relationship").grid(row=2, column=0, padx=12, pady=(12, 0))
        self.combobox_relationship = Combobox(self, values=[relationship["name"] for relationship in self.list_relationships], state="readonly")
        self.combobox_relationship.grid(row=2, column=1, padx=12, pady=(12, 0))

        self.button_save = Button(self, text="Save", command=self.save)
        self.button_save.grid(row=3, column=0, columnspan=2, padx=12, pady=12)

    def save(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        relationship = self.option_selected(self.list_relationships, self.combobox_relationship)["id"]

        is_valid = self.validate(name=name, phone=phone, relationship=relationship)

        if not is_valid:
            return
        
        if self.emergency_contact:
            id = self.emergency_contact["id"]
            EmergencyContact().update(id, name, relationship, phone)
            messagebox.showinfo("Success", "Emergency Contact updated successfully")
        else:
            id_user = self.user["id"]
            EmergencyContact(name, relationship, phone).save(id_user)
            messagebox.showinfo("Success", "Emergency Contact created successfully")

    def config(self):
        self.resizable(False, False)
        if self.emergency_contact:
            self.title("Update Emergency Contact")
        else:
            self.title("Create Emergency Contact")

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def set_data_in_inputs(self):
        if not self.emergency_contact:
            return

        self.entry_name.insert(0, self.emergency_contact["name"])
        self.entry_phone.insert(0, self.emergency_contact["phone"])
        self.combobox_relationship.set(self.emergency_contact["relationship"])

    def validate(self, **kwargs):
        required_inputs = ["name", "phone"]
        required_selections = ["relationship"]

        PHONE_REGEX = r'^[2-9] \d{3,4} \d{4}$'

        for input_name in required_inputs:
            if not kwargs[input_name]:
                messagebox.showwarning("Warning", f"{input_name.capitalize()} is required")
                return False
            
        for selection_name in required_selections:
            if not kwargs[selection_name]:
                messagebox.showwarning("Warning", f"{selection_name.capitalize()} is required")
                return False
            
        if not re.match(PHONE_REGEX, kwargs.get('phone')):
            messagebox.showerror("Error", "Invalid phone format (ex: 9 1234 5678 or 2 1234 5678)")
            return False

        return True
    
    def option_selected(self, list, box):
        selected_name = box.get()
        return next((item for item in list if item["name"] == selected_name), None)