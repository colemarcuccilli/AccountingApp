from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog
from views.styles import styles

class Tax:
    def __init__(self, parent, businesses):
        self.parent = parent
        self.businesses = businesses
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Tax")
        label.setStyleSheet(styles["header"])
        layout.addWidget(label)

        self.business_selector = QComboBox()
        self.update_businesses()
        layout.addWidget(self.business_selector)

        self.add_tax_form(layout)

        self.export_button = QPushButton("Export Taxes")
        self.export_button.setStyleSheet(styles["button"])
        self.export_button.clicked.connect(self.export_taxes)
        layout.addWidget(self.export_button)

        self.import_button = QPushButton("Import Taxes")
        self.import_button.setStyleSheet(styles["button"])
        self.import_button.clicked.connect(self.import_taxes)
        layout.addWidget(self.import_button)

        self.parent.setLayout(layout)

    def update_businesses(self):
        self.business_selector.clear()
        self.business_selector.addItems(self.businesses.keys())

    def add_tax_form(self, layout):
        form_layout = QVBoxLayout()

        self.tax_type_input = QLineEdit()
        self.tax_type_input.setPlaceholderText("Tax Type")
        self.tax_type_input.setStyleSheet(styles["input"])
        form_layout.addWidget(self.tax_type_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.amount_input.setStyleSheet(styles["input"])
        form_layout.addWidget(self.amount_input)

        add_tax_button = QPushButton("Add Tax")
        add_tax_button.setStyleSheet(styles["button"])
        add_tax_button.clicked.connect(self.add_tax)
        form_layout.addWidget(add_tax_button)

        layout.addLayout(form_layout)

    def add_tax(self):
        tax_type = self.tax_type_input.text()
        amount = self.amount_input.text()

        if tax_type and amount:
            selected_business = self.business_selector.currentText()
            if selected_business:
                tax_item = {"tax_type": tax_type, "amount": amount}
                if "taxes" not in self.businesses[selected_business]:
                    self.businesses[selected_business]["taxes"] = []
                self.businesses[selected_business]["taxes"].append(tax_item)
                self.clear_form()

    def clear_form(self):
        self.tax_type_input.clear()
        self.amount_input.clear()

    def export_taxes(self):
        selected_business = self.business_selector.currentText()
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Export Taxes", "", "CSV Files (*.csv)")
        if selected_business and file_path:
            self.data_handler.save_taxes(file_path, selected_business)

    def import_taxes(self):
        selected_business = self.business_selector.currentText()
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Import Taxes", "", "CSV Files (*.csv)")
        if selected_business and file_path:
            self.data_handler.load_taxes(file_path, selected_business)
