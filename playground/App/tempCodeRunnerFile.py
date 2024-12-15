def show_medical_history(self):
        label = tk.Label(self.content_frame, text="Medical History", font=("Arial", 24))
        label.pack(pady=20)

        # Create a Treeview widget for displaying the medical records
        tree = ttk.Treeview(self.content_frame, columns=("Patient Name", "Medical Record"), show="headings")
        tree.heading("Patient Name", text="Patient Name")
        tree.heading("Medical Record", text="Medical Record")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the treeview
        tree.pack(pady=10, fill="both", expand=True)

        # Fetch and display medical records
        patients = show_medical_records()  # Call the imported function
        print(f"Fetched patients: {patients}")  # Debugging output to check what is returned

        if not patients:  # Check if patients list is empty
            print("No patients found.")
            tree.insert("", "end", values=("No patients found", ""))
        else:
            for patient in patients:
                patient_name = f"{patient['first_name']} {patient['last_name']}"
                print(f"Processing patient: {patient_name}")  # Debugging output
                try:
                    medical_records = patient.get('medical_records', [])

                    if not medical_records:
                        tree.insert("", "end", values=(patient_name, "No records found"))
                        print(f"No records found for {patient_name}")  # Debugging output
                    else:
                        # Join medical records into a single string to fit into the Treeview cell
                        medical_record_text = " | ".join(medical_records)
                        tree.insert("", "end", values=(patient_name, medical_record_text))
                        print(f"Medical records for {patient_name}: {medical_record_text}")  # Debugging output

                except Exception as e:
                    print(f"Error processing patient {patient_name}: {str(e)}")  # Debugging output
                    tree.insert("", "end", values=(patient_name, f"Error: {str(e)}"))
