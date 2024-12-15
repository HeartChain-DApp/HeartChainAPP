import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import json
from All_Patients import fetch_and_save_patient_data

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Tkinter Application")
        self.geometry("800x600")

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
