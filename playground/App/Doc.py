import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import json
from All_Patients import fetch_and_save_patient_data
from All_Audits import fetch_audit_logs
import datetime

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Tkinter Application")
        self.geometry("1300x600")

        self.navbar = CustomNavigationBar(self, master=self)
        self.navbar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def on_button_click(self, text):
        for widget in self.content_frame.winfo_children():
            widget.destroy()



        # Update content based on the button clicked
        if text == "Home":
            self.show_home()
        elif text == "Patients Details":
            self.show_patient_details()
        elif text == "View Medical History":
            self.show_medical_history()
        elif text == "Clients":
            self.show_clients()
        elif text == "All Patients":
            self.show_all_patients()
        elif text == "Audit":
            self.show_audit()




    def show_home(self):
        label = tk.Label(self.content_frame, text="Welcome to the Home page!", font=("Arial", 24))
        label.pack(pady=20)




    def show_patient_details(self):
        label = tk.Label(self.content_frame, text="Patient Details", font=("Arial", 24))
        label.pack(pady=20)





    def show_medical_history(self):
        label = tk.Label(self.content_frame, text="Medical History", font=("Arial", 24))
        label.pack(pady=20)




    def show_clients(self):
        label = tk.Label(self.content_frame, text="Clients", font=("Arial", 24))
        label.pack(pady=20)




    def show_all_patients(self):
        label = tk.Label(self.content_frame, text="All Patients", font=("Arial", 24))
        label.pack(pady=20)
        fetch_and_save_patient_data()
        columns = ("Patient Address", "First Name", "Last Name", "Birth Date", "Address Details")    # a Tree view with column names to match the json file 
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        try:
            with open('patients_data.json', 'r') as file:
                patients_data = json.load(file)
            for patient in patients_data:
                tree.insert("", tk.END, values=(patient["Patient Address"], patient["First Name"], 
                                                patient["Last Name"], patient["Birth Date"], 
                                                patient["Address Details"]))
        except Exception as e:
            print(f"Error loading patients data: {e}")

        tree.pack(pady=20, fill=tk.X)







    def show_audit(self):
        label = tk.Label(self.content_frame, text="Audit", font=("Arial", 24))
        label.pack(pady=20)
        
        # Add ComboBox for Action Type selection
        action_type_label = tk.Label(self.content_frame, text="Filter by Action Type:")
        action_type_label.pack(pady=10)
        
        action_types = ["All", "Creation", "Permission", "Update"]  # Add all available Action Types
        action_type_combobox = ttk.Combobox(self.content_frame, values=action_types)
        action_type_combobox.set("All")  # Set default selection to "All"
        action_type_combobox.pack(pady=5)
        
        # Define the columns for the Treeview widget
        columns = ("Timestamp", "Action", "User", "Record Hash", "Action Type")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        # Set up the column headings and their width
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        # Fetch the audit logs
        audit_logs = fetch_audit_logs()

        # Function to filter and update the Treeview based on selected Action Type
        def update_audit_logs():
            selected_action_type = action_type_combobox.get()

            # If "All" is selected, show all logs, else filter by selected Action Type
            if selected_action_type == "All":
                filtered_logs = audit_logs
            else:
                filtered_logs = [audit for audit in audit_logs if audit.get("action_type") == selected_action_type]
            
            # Clear the Treeview before inserting filtered logs
            for item in tree.get_children():
                tree.delete(item)

            # Insert the filtered audit logs into the Treeview
            if filtered_logs:
                for audit in filtered_logs:
                    # Make sure to access values as dictionary keys
                    tree.insert("", "end", values=(audit.get("timestamp"), audit.get("action"), audit.get("user"), audit.get("record_hash"), audit.get("action_type")))
            else:
                print("No audit logs available.")  

        # Add a button to refresh the display based on the selected Action Type
        refresh_button = tk.Button(self.content_frame, text="Refresh", command=update_audit_logs)
        refresh_button.pack(pady=10)

        # Pack the Treeview widget into the window
        tree.pack(pady=20, fill="both", expand=True)

        # Initial load of all audit logs
        update_audit_logs()








class CustomNavigationBar(ctk.CTkFrame):
    def __init__(self, app, master=None):
        super().__init__(master, fg_color="#2C3E50", width=200, height=600)  # Use fg_color instead of bg
        self.app = app
        self.create_buttons()
    def create_buttons(self):
        buttons = ["Home", "Patients Details", "View Medical History", "Clients", "All Patients", "Audit"]
        button_widgets = []
        for btn_text in buttons:
            btn = ctk.CTkButton(self, text=btn_text, fg_color="#3498DB", command=lambda text=btn_text: self.button_click(text))
            button_widgets.append(btn)
        total_button_height = sum(btn.winfo_reqheight() for btn in button_widgets) + len(button_widgets) * 10  # Add padding between buttons
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
