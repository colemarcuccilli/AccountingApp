from PyQt5.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFormLayout
from styles import styles

class TransactionWizard(QWizard):
    def __init__(self, businesses):
        super().__init__()
        self.businesses = businesses

        self.setWindowTitle("Transaction Wizard")
        self.addPage(self.create_intro_page())
        self.addPage(self.create_details_page())
        self.addPage(self.create_confirmation_page())

    def create_intro_page(self):
        page = QWizardPage()
        page.setTitle("Introduction")
        
        layout = QVBoxLayout()
        label = QLabel("This wizard will help you enter a new transaction.")
        layout.addWidget(label)
        
        page.setLayout(layout)
        return page

    def create_details_page(self):
        page = QWizardPage()
        page.setTitle("Transaction Details")
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date (YYYY-MM-DD)")
        self.date_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Date:"), self.date_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Description:"), self.description_input)

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account")
        self.account_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Account:"), self.account_input)

        self.debit_account_input = QLineEdit()
        self.debit_account_input.setPlaceholderText("Money In (Debit Account)")
        self.debit_account_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Money In (Debit Account):"), self.debit_account_input)

        self.credit_account_input = QLineEdit()
        self.credit_account_input.setPlaceholderText("Money Out (Credit Account)")
        self.credit_account_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Money Out (Credit Account):"), self.credit_account_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.amount_input.setStyleSheet(styles["input"])
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        layout.addLayout(form_layout)
        page.setLayout(layout)
        return page

    def create_confirmation_page(self):
        page = QWizardPage()
        page.setTitle("Confirmation")
        
        layout = QVBoxLayout()
        label = QLabel("Click Finish to add the transaction.")
        layout.addWidget(label)
        
        finish_button = QPushButton("Finish")
        finish_button.clicked.connect(self.add_transaction)
        layout.addWidget(finish_button)
        
        page.setLayout(layout)
        return page

    def add_transaction(self):
        date = self.date_input.text()
        description = self.description_input.text()
        account = self.account_input.text()
        debit_account = self.debit_account_input.text()
        credit_account = self.credit_account_input.text()
        amount = self.amount_input.text()

        if date and description and account and (debit_account or credit_account) and amount:
            selected_business = self.business_selector.currentText()
            if selected_business:
                transaction = {
                    "date": date,
                    "description": description,
                    "account": account,
                    "debit_account": debit_account,
                    "credit_account": credit_account,
                    "amount": amount
                }
                if "transactions" not in self.businesses[selected_business]:
                    self.businesses[selected_business]["transactions"] = []
                self.businesses[selected_business]["transactions"].append(transaction)
                self.close()
