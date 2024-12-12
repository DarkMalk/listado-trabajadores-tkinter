from tkinter import Tk, messagebox
from tkinter.ttk import Treeview, Button, Labelframe
from models import EmergencyContact
from .create_or_update_emergency_contact import CreateOrUpdateEmergencyContactView

class ManageEmergencyContactView(Tk):
    list_emergency_contact = []
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.widget_treeview()
        self.widgets_options()

        self.set_data()

        self.config()
        self.mainloop()

    def widget_treeview(self):
        COLUMNS = ("name", "relationship", "phone")
        self.treeview = Treeview(self, columns=COLUMNS, show="headings")
        self.treeview.heading("name", text="Name")
        self.treeview.heading("relationship", text="Relationship")
        self.treeview.heading("phone", text="Phone")
        self.treeview.grid(row=0, column=0, columnspan=2, padx=12, pady=(12, 0))

        self.treeview.column("name", width=150, anchor="center")
        self.treeview.column("relationship", width=150, anchor="center")
        self.treeview.column("phone", width=150, anchor="center")

        self.treeview.grid_columnconfigure(0, weight=1)
        self.treeview.grid_columnconfigure(1, weight=1)
        self.treeview.grid_columnconfigure(2, weight=1)

    def set_data(self):
        self.list_emergency_contact = EmergencyContact().get_all(self.user["id"])

        self.treeview.delete(*self.treeview.get_children())
        for emergency_contact in self.list_emergency_contact:
            self.treeview.insert("", "end", values=(emergency_contact['name'], emergency_contact['relationship'], emergency_contact['phone']))

    def widgets_options(self):
        label_frame = Labelframe(self, text="Options")
        label_frame.grid(row=1, column=0, columnspan=2, padx=12, pady=12)

        self.button_add = Button(label_frame, text="Add", command=self.add)
        self.button_add.grid(row=0, column=0, padx=12, pady=12)

        self.button_delete = Button(label_frame, text="Delete", command=self.delete)
        self.button_delete.grid(row=0, column=1, padx=12, pady=12)

        self.button_update = Button(label_frame, text="Update", command=self.update)
        self.button_update.grid(row=0, column=2, padx=12, pady=12)

    def add(self):
        CreateOrUpdateEmergencyContactView(self.user, on_close_callback=self.set_data)

    def delete(self):
        emer_contact_selected = self.selected_emergency_contact()

        if not emer_contact_selected:
            messagebox.showwarning("Warning", "Select an emergency contact")
            return

        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete {emer_contact_selected['name']}?")
        if confirm:
            EmergencyContact().delete(emer_contact_selected["id"])
            self.set_data()

    def update(self):
        emer_contact_selected = self.selected_emergency_contact()

        if not emer_contact_selected:
            messagebox.showwarning("Warning", "Select an emergency contact")
            return
        
        CreateOrUpdateEmergencyContactView(self.user, emer_contact_selected, on_close_callback=self.set_data)

    def selected_emergency_contact(self):
        selected_tuple = self.treeview.selection()

        if not selected_tuple:
            return None
        
        selected = self.treeview.index(selected_tuple[0])

        for index, emer_contact in enumerate(self.list_emergency_contact):
            if selected == index:
                return emer_contact

    def config(self):
        self.resizable(False, False)
        self.title('Manage Emergency Contact')