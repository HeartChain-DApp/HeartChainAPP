def fetch_patient_details(self):
        try:
            # Fetch all patient addresses from the contract
            patient_addresses = contract.functions.viewAllPatients().call()
            
            if not patient_addresses:
                self.results_browser.setText("No patients found.")
                return
            
            result_text = "Patients List:\n"
            
            # Loop through each patient address
            for patient_address in patient_addresses:
                # Fetch patient data using the address
                patient = contract.functions.patients(patient_address).call()

                # Debugging: Print the raw patient data to inspect
                print(f"Raw patient data for {patient_address}: {patient}")

                # Ensure that the patient data exists and has the expected structure
                if len(patient) >= 6:  # We expect at least 6 elements (first name, last name, etc.)
                    first_name = patient[0] if patient[0] else "N/A"
                    last_name = patient[1] if patient[1] else "N/A"
                    birth_date = patient[2] if patient[2] else "N/A"
                    address_details = patient[3] if patient[3] else "N/A"
                    medical_history = ', '.join(patient[5]) if patient[5] and len(patient[5]) > 0 else "No medical history available"

                    result_text += f"\nPatient Address: {patient_address}\n"
                    result_text += f"First Name: {first_name}\n"
                    result_text += f"Last Name: {last_name}\n"
                    result_text += f"Birth Date: {birth_date}\n"
                    result_text += f"Address: {address_details}\n"
                    result_text += f"Medical History: {medical_history}\n"
                else:
                    result_text += f"Error fetching details for patient address: {patient_address} (data incomplete)\n"

            self.results_browser.setText(result_text)

        except Exception as e:
            self.results_browser.setText(f"Error fetching patient details: {e}")