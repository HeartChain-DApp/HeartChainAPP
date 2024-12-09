import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt

class DecentralizedAuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Decentralized Authentication')
        self.setGeometry(100, 100, 400, 400)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Form widgets
        self.name_input = QLineEdit(self)
        self.surname_input = QLineEdit(self)
        self.age_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.specialty_input = QLineEdit(self)
        self.access_input = QComboBox(self)
        self.access_input.addItem('True')
        self.access_input.addItem('False')

        # Buttons
        self.register_patient_button = QPushButton('Register as Patient', self)
        self.register_doctor_button = QPushButton('Register as Doctor', self)
        self.authenticate_patient_button = QPushButton('Authenticate as Patient', self)
        self.authenticate_doctor_button = QPushButton('Authenticate as Doctor', self)

        # Result display
        self.result_label = QLabel(self)

        # Add widgets to layout
        self.form_layout.addRow('Name:', self.name_input)
        self.form_layout.addRow('Surname:', self.surname_input)
        self.form_layout.addRow('Age:', self.age_input)
        self.form_layout.addRow('Password:', self.password_input)
        self.form_layout.addRow('Specialty (Doctor only):', self.specialty_input)
        self.form_layout.addRow('Access (Doctor only):', self.access_input)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.register_patient_button)
        self.main_layout.addWidget(self.register_doctor_button)
        self.main_layout.addWidget(self.authenticate_patient_button)
        self.main_layout.addWidget(self.authenticate_doctor_button)
        self.main_layout.addWidget(self.result_label)

        self.setLayout(self.main_layout)

        # Connect buttons to functions
        self.register_patient_button.clicked.connect(self.register_patient)
        self.register_doctor_button.clicked.connect(self.register_doctor)
        self.authenticate_patient_button.clicked.connect(self.authenticate_patient)
        self.authenticate_doctor_button.clicked.connect(self.authenticate_doctor)

    def register_patient(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        age = int(self.age_input.text())
        password = self.password_input.text()

        # Register the patient (to be implemented with actual blockchain interaction)
        # For now, just display the result in the label
        self.result_label.setText(f"Patient {name} {surname} registered successfully!")

    def register_doctor(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        specialty = self.specialty_input.text()
        access = self.access_input.currentText() == 'True'
        password = self.password_input.text()

        # Register the doctor (to be implemented with actual blockchain interaction)
        # For now, just display the result in the label
        self.result_label.setText(f"Doctor {name} {surname} registered successfully with specialty: {specialty}!")

    def authenticate_patient(self):
        password = self.password_input.text()
        # Authenticate the patient (to be implemented with actual blockchain interaction)
        # For now, just display a success message
        self.result_label.setText("Patient authenticated successfully!")

    def authenticate_doctor(self):
        password = self.password_input.text()
        # Authenticate the doctor (to be implemented with actual blockchain interaction)
        # For now, just display a success message
        self.result_label.setText("Doctor authenticated successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecentralizedAuthApp()
    window.show()
    sys.exit(app.exec_())
