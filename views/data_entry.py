from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtGui import QFont
from styles import styles

class DataEntry(QWidget):
    def __init__(self, parent, businesses):
        super().__init__(parent)
        self.businesses = businesses
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Data Entry")
        title.setStyleSheet(styles["header"])
        title.setFont(QFont('Arial', 24))
        layout.addWidget(title)

        self.business_selector = QComboBox()
        self.business_selector.addItems(self.businesses.keys())
        self.business_selector.currentTextChanged.connect(self.update_account_dropdowns)
        layout.addWidget(self.business_selector)

        form_layout = QFormLayout()
        self.date_input = QLineEdit()
        self.description_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.debit_account_dropdown = QComboBox()
        self.credit_account_dropdown = QComboBox()
        
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Debit Account:", self.debit_account_dropdown)
        form_layout.addRow("Credit Account:", self.credit_account_dropdown)
        
        layout.addLayout(form_layout)

        save_button = QPushButton("Save Transaction")
        save_button.clicked.connect(self.save_transaction)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.update_account_dropdowns(self.business_selector.currentText())

    def update_account_dropdowns(self, business_name):
        if business_name in self.businesses:
            chart_of_accounts = self.businesses[business_name]["chart_of_accounts"]
            self.debit_account_dropdown.clear()
            self.credit_account_dropdown.clear()
            for account_category, accounts in chart_of_accounts.items():
                for account_number, account_name in accounts.items():
                    self.debit_account_dropdown.addItem(f"{account_number} {account_name}")
                    self.credit_account_dropdown.addItem(f"{account_number} {account_name}")

    def save_transaction(self):
        business_name = self.business_selector.currentText()
        if business_name in self.businesses:
            transaction = {
                "date": self.date_input.text(),
                "description": self.description_input.text(),
                "amount": self.amount_input.text(),
                "debit_account": self.debit_account_dropdown.currentText(),
                "credit_account": self.credit_account_dropdown.currentText()
            }
            self.businesses[business_name]["transactions"].append(transaction)
            self.parent().data_handler.save_data(self.businesses)
            QMessageBox.information(self, "Success", "Transaction saved successfully.")
