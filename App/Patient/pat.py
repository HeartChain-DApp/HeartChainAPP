import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import json
import datetime
from All_Audits import fetch_audit_logs
from tkinter import PhotoImage
from PIL import Image, ImageTk
from All_Doc import fetch_and_save_doctor_data
from docaddress import doct_addrs
from docdetailsspec import doc_details
from manageacces import manage_access_overall
from mymedical import show_medical_records

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patient App")
        self.geometry("1300x600")

        self.navbar = CustomNavigationBar(self, master=self)
        self.navbar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def on_button_click(self, text):
        for widget in self.content_frame.winfo_children():
            widget.destroy()


        if text == "Home":
            self.show_home()
        elif text == "View Medical History":
            self.view_medical_history()
        elif text == "Manage Access":
            self.manage_access()
        elif text == "All Doctors":
            self.show_doctors()
        elif text == "History":
            self.show_audit()





    def show_home(self):
        
        welcome_label = tk.Label(self.content_frame, text="Welcome back Doctor", font=("Arial", 24), fg="green")
        welcome_label.pack(pady=20)




    def view_medical_history(self):
        label = ctk.CTkLabel(self.content_frame, text="Medical History by Your Doctor's Authorization", font=("Arial", 24))
        label.pack(pady=10)

        medical_records = show_medical_records()  

        treeview = ttk.Treeview(self.content_frame)
        treeview.pack(fill="both", expand=True)

        treeview["columns"] = ("Record")
        treeview.column("#0", width=0, stretch="no")
        treeview.column("Record", anchor="w", width=500)

        treeview.heading("#0", text="", anchor="w")
        treeview.heading("Record", text="Medical Record", anchor="w")

        if isinstance(medical_records, list):
            for record in medical_records:
                treeview.insert("", "end", values=(record,))
        else:
            treeview.insert("", "end", values=("No medical records found."))



    def manage_access(self):
        label = ctk.CTkLabel(self.content_frame, text="Medical History", font=("Arial", 24))
        label.pack(pady=20)
        doctor_addresses = doct_addrs()
        doctor_dropdown = ctk.CTkComboBox(self.content_frame, values=doctor_addresses, width=200)
        doctor_dropdown.pack(pady=10) 
        treeview = ttk.Treeview(self.content_frame, columns=("Detail", "Value"), show="headings",height=5)
        treeview.heading("Detail", text="Detail")
        treeview.heading("Value", text="Value")
        treeview.column("Detail", stretch=True, width=200)  
        treeview.column("Value", stretch=True, width=200)   

        treeview.pack(pady=20, fill='x', expand=True)  
        def handle_access_action():
            selected_address = doctor_dropdown.get()
            details = doc_details(selected_address)
            for item in treeview.get_children():
                treeview.delete(item)

            if isinstance(details, list):
                for idx, value in enumerate(details):
                    treeview.insert("", "end", values=(f"Field {idx+1}", value))  
            else:
                for detail, value in details.items():
                    treeview.insert("", "end", values=(detail, value))
            authorize_button = ctk.CTkButton(self.content_frame, text="Authorize", command=lambda: self.handle_grant_revoke_action('authorize', selected_address))
            revoke_button = ctk.CTkButton(self.content_frame, text="Revoke", command=lambda: self.handle_grant_revoke_action('revoke', selected_address))
            authorize_button.pack(pady=10)
            revoke_button.pack(pady=10)
        action_button = ctk.CTkButton(self.content_frame, text="Select Doctor", command=handle_access_action)
        action_button.pack(pady=10)

    def handle_grant_revoke_action(self, action, doctor_address):
        patient_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
        tx_hash = manage_access_overall(patient_address, doctor_address, action)
        

        
        
        

    def sort_column(treeview, col):
        items = [treeview.item(item)["values"] for item in treeview.get_children()]
        sorted_items = sorted(items, key=lambda x: x[0] if col == "Patient Name" else x[1])

       



    def show_doctors(self):
        label = ctk.CTkLabel(self.content_frame, text="All Doctors", font=("Arial", 24))
        label.pack(pady=20)
        doctors_data = fetch_and_save_doctor_data()  # Fetch the list of doctors

        if not doctors_data:
            print("No doctors available.")
            return

        # Ensure that the treeview widget is created only once
        if not hasattr(self, 'tree'):
            self.tree = ttk.Treeview(self.content_frame, columns=("First Name", "Last Name", "Specialty", "Address"), show="headings")
            self.tree.heading("First Name", text="First Name")
            self.tree.heading("Last Name", text="Last Name")
            self.tree.heading("Specialty", text="Specialty")
            self.tree.heading("Address", text="Address")

            self.tree.column("First Name", width=150)
            self.tree.column("Last Name", width=150)
            self.tree.column("Specialty", width=150)
            self.tree.column("Address", width=200)

            self.tree.pack(fill=tk.BOTH, expand=True)

        # Clear any existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new doctor data into the treeview
        for doctor in doctors_data:
            self.tree.insert("", "end", values=(doctor["firstName"], doctor["lastName"], doctor["specialty"], doctor["doctorAddress"]))



    def show_all_patients(self):
        label = tk.Label(self.content_frame, text="All Patients", font=("Arial", 24))
        label.pack(pady=20)
        







    def show_audit(self):
        label = tk.Label(self.content_frame, text="Audit", font=("Arial", 24))
        label.pack(pady=20)
        action_type_label = tk.Label(self.content_frame, text="Filter by Action Type:")
        action_type_label.pack(pady=10)
        
        action_types = ["All", "Creation", "Permission", "Update"]
        action_type_combobox = ttk.Combobox(self.content_frame, values=action_types)
        action_type_combobox.set("All")
        action_type_combobox.pack(pady=5)
        
        columns = ("Timestamp", "Action", "User", "Record Hash", "Action Type")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        # Assuming fetch_audit_logs() returns the audit logs in the form of a list of dictionaries
        audit_logs = fetch_audit_logs()

        def update_audit_logs():
            selected_action_type = action_type_combobox.get()

            # Filter the logs for a specific user (0x70997970C51812dc3A010C7d01b50e0d17dc79C8)
            filtered_logs = [audit for audit in audit_logs if audit.get("user") == "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"]

            if selected_action_type != "All":
                filtered_logs = [audit for audit in filtered_logs if audit.get("action_type") == selected_action_type]

            for item in tree.get_children():
                tree.delete(item)

            if filtered_logs:
                for audit in filtered_logs:
                    tree.insert("", "end", values=(audit.get("timestamp"), audit.get("action"), audit.get("user"), audit.get("record_hash"), audit.get("action_type")))
            else:
                print("No audit logs available.")

        refresh_button = tk.Button(self.content_frame, text="Refresh", command=update_audit_logs)
        refresh_button.pack(pady=10)

        tree.pack(pady=20, fill="both", expand=True)
        
        update_audit_logs()








class CustomNavigationBar(ctk.CTkFrame):
    def __init__(self, app, master=None):
        super().__init__(master, fg_color="#2C3E50", width=200, height=600)  
        self.app = app
        self.create_buttons()
    def create_buttons(self):
        buttons = ["Home", "View Medical History", "Manage Access", "All Doctors", "History"]
        button_widgets = []
        for btn_text in buttons:
            btn = ctk.CTkButton(self, text=btn_text, fg_color="#3498DB", command=lambda text=btn_text: self.button_click(text))
            button_widgets.append(btn)
        total_button_height = sum(btn.winfo_reqheight() for btn in button_widgets) + len(button_widgets) * 10  
        total_space = self.winfo_height()
        top_padding = (total_space - total_button_height) // 2
        bottom_padding = total_space - total_button_height - top_padding
        self.grid_rowconfigure(0, weight=1, minsize=top_padding)  
        self.grid_rowconfigure(len(button_widgets) + 1, weight=1, minsize=bottom_padding) 
        for btn in button_widgets:
            btn.pack(side=tk.TOP, fill=tk.X, padx=40, pady=10)

    def button_click(self, text):
        self.app.on_button_click(text)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
