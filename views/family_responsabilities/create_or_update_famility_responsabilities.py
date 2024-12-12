from tkinter import Tk, messagebox
from tkinter.ttk import Button, Label, Entry, Combobox
from models import Gender, Relationships, FamilyResponsabilities
import re

class CreateOrUpdateFamilityResponsabilities(Tk):
    list_genders = []
    list_relationships = []
    def __init__(self, family_responsability=None, on_close_callback=None, id_user=None):
        super().__init__()
        self.family_responsability = family_responsability
        self.on_close_callback = on_close_callback
        self.id_user = id_user

        self.list_genders = Gender().get_all()
        self.list_relationships = Relationships().get_all()

        self.widgets()
        self.config()
        self.set_data_in_inputs()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def widgets(self):
        Label(self, text="Name").grid(row=0, column=0, padx=12, pady=(12, 0))
        self.entry_name = Entry(self)
        self.entry_name.grid(row=0, column=1, padx=12, pady=(12, 0))

        Label(self, text="Rut").grid(row=1, column=0, padx=12, pady=(12, 0))
        self.entry_rut = Entry(self)
        self.entry_rut.grid(row=1, column=1, padx=12, pady=(12, 0))

        Label(self, text="Gender").grid(row=2, column=0, padx=12, pady=(12, 0))
        self.combo_gender = Combobox(self, values=[gender["name"] for gender in self.list_genders], state="readonly")
        self.combo_gender.grid(row=2, column=1, padx=12, pady=(12, 0))

        Label(self, text="Relationship").grid(row=3, column=0, padx=12, pady=(12, 0))
        self.combo_relationship = Combobox(self, values=[relationship["name"] for relationship in self.list_relationships], state="readonly")
        self.combo_relationship.grid(row=3, column=1, padx=12, pady=(12, 0))

        self.btn_save = Button(self, text="Save", command=self.save)
        self.btn_save.grid(row=4, column=0, columnspan=2, padx=12, pady=12)

    def save(self):
        name = self.entry_name.get()
        rut = self.entry_rut.get()

        relationship = self.option_selected(self.list_relationships, self.combo_relationship)["id"]
        gender = self.option_selected(self.list_genders, self.combo_gender)["id"]

        is_valid = self.validate(name=name, rut=rut, relationship=relationship, gender=gender)

        if not is_valid:
            return
        
        if self.family_responsability:
            try:
                FamilyResponsabilities().update(self.family_responsability["id"], name, rut, relationship, gender)
                messagebox.showinfo("Success", "Family responsability updated successfully")
            except Exception as e:
                messagebox.showerror("Error", "An error occurred while updating the family responsability")
        else:
            try:
                FamilyResponsabilities(name, rut, relationship, gender).save(self.id_user)
                messagebox.showinfo("Success", "Family responsability created successfully")
            except Exception as e:
                messagebox.showerror("Error", "An error occurred while creating the family responsability")
    

    def config(self):
        self.resizable(False, False)
        if self.family_responsability:
            self.title("Update Famility Responsabilities")
        else:
            self.title("Create Famility Responsabilities")

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()

    def set_data_in_inputs(self):
        if not self.family_responsability:
            return
        
        self.entry_name.insert(0, self.family_responsability["name"])
        self.entry_rut.insert(0, self.family_responsability["rut"])
        self.combo_gender.set(self.family_responsability["gender"])
        self.combo_relationship.set(self.family_responsability["relationship"])

    def validate(self, **kwargs):
        required_fields = ["name", "rut"]
        selection_fields = ["gender", "relationship"]

        REGEX_RUT = r"^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$"

        for field in required_fields:
            if not kwargs.get(field):
                messagebox.showerror("Error", f"The field '{field}' is required")
                return False

        for field in selection_fields:
            if not kwargs.get(field):
                messagebox.showerror("Error", f"The selection '{field}' is required")
                return False
            
        if not re.match(REGEX_RUT, kwargs.get('rut')):
            messagebox.showerror("Error", "Invalid RUT format (ex: 12.345.678-9)")
            return False

        return True

    def option_selected(self, list, box):
        selected_name = box.get()
        return next((item for item in list if item["name"] == selected_name), None)
