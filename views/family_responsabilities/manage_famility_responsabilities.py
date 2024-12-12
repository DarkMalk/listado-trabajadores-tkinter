from tkinter import Tk, messagebox
from tkinter.ttk import Treeview, Button, Labelframe
from models import FamilyResponsabilities
from .create_or_update_famility_responsabilities import CreateOrUpdateFamilityResponsabilities

class ManageFamilyResponsabilitiesView(Tk):
    def __init__(self, user, on_close_callback=None, ):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.user = user
        self.list_family_responsabilities = []


        self.widget_treeview()
        self.set_data()
        self.widget_options()

        self.config()
        self.mainloop()

    def widget_treeview(self):
        self.treeview = Treeview(self, columns=("name", "rut", "relationship", "gender"), show="headings")
        self.treeview.grid(row=0, column=0, columnspan=4, padx=24, pady=(24, 12))

        self.treeview.heading("name", text="Name")
        self.treeview.heading("rut", text="Rut")
        self.treeview.heading("relationship", text="Relationship")
        self.treeview.heading("gender", text="Gender")

        self.treeview.column("name", width=150, anchor="center")
        self.treeview.column("rut", width=150, anchor="center")
        self.treeview.column("relationship", width=150, anchor="center")
        self.treeview.column("gender", width=150, anchor="center")

        self.treeview.grid_columnconfigure(0, weight=1)
        self.treeview.grid_columnconfigure(1, weight=1)
        self.treeview.grid_columnconfigure(2, weight=1)
        self.treeview.grid_columnconfigure(3, weight=1)

    def widget_options(self):
        label_frame = Labelframe(self, text="Options")
        label_frame.grid(row=2, column=2, columnspan=2, padx=24, pady=(0, 12))

        self.btn_new = Button(label_frame, text="New Family Member", command=self.open_new_family_member)
        self.btn_new.grid(row=0, column=0, padx=12, pady=(4, 12))
        
        self.btn_delete = Button(label_frame, text="Delete Family Member", command=self.delete_family_member)
        self.btn_delete.grid(row=0, column=1, padx=12, pady=(4, 12))

        self.btn_update = Button(label_frame, text="Update Family Member", command=self.update_family_member)
        self.btn_update.grid(row=0, column=2, padx=12, pady=(4, 12))

    
    def open_new_family_member(self):
        CreateOrUpdateFamilityResponsabilities(on_close_callback=self.set_data, id_user=self.user["id"])

    def delete_family_member(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showwarning("Error", "Select a family member")
            return
        
        family_responsabilities_id = self.list_family_responsabilities[index]["id"]

        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this family member?")

        if not confirm:
            return

        try:
            FamilyResponsabilities().delete(family_responsabilities_id)
            self.set_data()
            messagebox.showinfo("Success", "Family member deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while deleting the user")
            print(e)

    def update_family_member(self):
        index = self.select_item()

        if index == -1 or index is None:
            messagebox.showwarning("Error", "Select a family member")
            return
        
        family_responsability = self.list_family_responsabilities[index]

        CreateOrUpdateFamilityResponsabilities(family_responsability, self.set_data, id_user=self.user["id"])

    def set_data(self):
        self.list_family_responsabilities = FamilyResponsabilities().get_all(self.user["id"])
        self.treeview.delete(*self.treeview.get_children())

        for family_responsability in self.list_family_responsabilities:
            self.treeview.insert("", "end", values=(family_responsability["name"], family_responsability["rut"], family_responsability["relationship"], family_responsability["gender"]))

    def config(self):
        self.title("Manage Family Responsabilities")
        self.resizable(False, False)

    def select_item(self):
        selected_item = self.treeview.selection()
        if selected_item:
            selected_id = selected_item[0]
            selected_values = self.treeview.item(selected_id, "values")

            return self.get_family_resp(selected_values)
        
    def get_family_resp(self, values):
        for index, family in enumerate(self.list_family_responsabilities):
            if family["name"] == values[0]:
                return index