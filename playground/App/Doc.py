import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import json
from All_Patients import fetch_and_save_patient_data
from All_Audits import fetch_audit_logs
from listingfollowing import fetch_patients_following_doctor
import datetime
from medical import show_medical_records

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
        tree = ttk.Treeview(self.content_frame, columns=("Patient Name", "Diagnosis", "Nurse", "Room", "Time"), show="headings")
        tree.heading("Patient Name", text="Patient Name")
        tree.heading("Diagnosis", text="Diagnosis")
        tree.heading("Nurse", text="Nurse")
        tree.heading("Room", text="Room")
        tree.heading("Time", text="Time")

        tree.column("Patient Name", width=150)
        tree.column("Diagnosis", width=200)
        tree.column("Nurse", width=150)
        tree.column("Room", width=100)
        tree.column("Time", width=100)

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(pady=10, fill="both", expand=True)

        patients = show_medical_records()  
        print(f"Fetched patients: {patients}")  

        if not patients: 
            print("No patients found.")
            tree.insert("", "end", values=("No patients found", "", "", "", ""))
        else:
            for patient in patients:
                patient_name = f"{patient['first_name']} {patient['last_name']}"
                print(f"Processing patient: {patient_name}") 
                try:
                    medical_records = patient.get('medical_records', [])

                    if not medical_records:
                        tree.insert("", "end", values=(patient_name, "No records found", "", "", ""))
                        print(f"No records found for {patient_name}") 
                    else:
                        for record in medical_records:
                            try:
                                diagnosis = record.split(",")[0].split(":")[1].strip() if "Diagnostic" in record else "N/A"
                                nurse = record.split(",")[1].split(":")[1].strip() if "Nurse" in record else "N/A"
                                room = record.split(",")[2].split(":")[1].strip() if "Room" in record else "N/A"
                                time = record.split(",")[3].split(":")[1].strip() if "Time" in record else "N/A"
                                tree.insert("", "end", values=(patient_name, diagnosis, nurse, room, time))
                                print(f"Medical records for {patient_name}: {diagnosis}, {nurse}, {room}, {time}") 

                            except Exception as e:
                                print(f"Error parsing medical record: {str(e)}")

                except Exception as e:
                    print(f"Error processing patient {patient_name}: {str(e)}")  
                    tree.insert("", "end", values=(patient_name, f"Error: {str(e)}", "", "", ""))




    def show_clients(self):
        doctor_index = 0
        patients = fetch_patients_following_doctor(doctor_index)

        label = tk.Label(self.content_frame, text="Clients", font=("Arial", 24))
        label.pack(pady=20)

        if not patients:
            no_patients_label = tk.Label(self.content_frame, text="No patients found for the given doctor.", font=("Arial", 14))
            no_patients_label.pack(pady=10)
        else:
            columns = ("First Name", "Last Name", "Birth Date", "Address", "Ethereum Address")

            tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
            tree.pack(pady=10, fill="both", expand=True)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor="w")

            for patient in patients:
                birth_date = patient['birth_date']
                tree.insert("", "end", values=(patient['first_name'], patient['last_name'], birth_date, patient['address_details'], patient['patient_address']))




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

        audit_logs = fetch_audit_logs()

        def update_audit_logs():
            selected_action_type = action_type_combobox.get()

            if selected_action_type == "All":
                filtered_logs = audit_logs
            else:
                filtered_logs = [audit for audit in audit_logs if audit.get("action_type") == selected_action_type]
            
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
        buttons = ["Home", "Patients Details", "View Medical History", "Clients", "All Patients", "Audit"]
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
