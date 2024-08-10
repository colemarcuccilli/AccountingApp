from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QFileDialog
from views.styles import styles

class Budget:
    def __init__(self, parent, businesses):
        self.parent = parent
        self.businesses = businesses
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Budget")
        label.setStyleSheet(styles["header"])
        layout.addWidget(label)

        self.business_selector = QComboBox()
        self.update_businesses()
        layout.addWidget(self.business_selector)

        self.add_budget_form(layout)

        self.export_button = QPushButton("Export Budget")
        self.export_button.setStyleSheet(styles["button"])
        self.export_button.clicked.connect(self.export_budget)
        layout.addWidget(self.export_button)

        self.import_button = QPushButton("Import Budget")
        self.import_button.setStyleSheet(styles["button"])
        self.import_button.clicked.connect(self.import_budget)
        layout.addWidget(self.import_button)

        self.parent.setLayout(layout)

    def update_businesses(self):
        self.business_selector.clear()
        self.business_selector.addItems(self.businesses.keys())

    def add_budget_form(self, layout):
        form_layout = QVBoxLayout()

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.category_input.setStyleSheet(styles["input"])
        form_layout.addWidget(self.category_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.amount_input.setStyleSheet(styles["input"])
        form_layout.addWidget(self.amount_input)

        add_budget_button = QPushButton("Add Budget")
        add_budget_button.setStyleSheet(styles["button"])
        add_budget_button.clicked.connect(self.add_budget)
        form_layout.addWidget(add_budget_button)

        layout.addLayout(form_layout)

    def add_budget(self):
        category = self.category_input.text()
        amount = self.amount_input.text()

        if category and amount:
            selected_business = self.business_selector.currentText()
            if selected_business:
                budget_item = {"category": category, "amount": amount}
                if "budget" not in self.businesses[selected_business]:
                    self.businesses[selected_business]["budget"] = []
                self.businesses[selected_business]["budget"].append(budget_item)
                self.clear_form()

    def clear_form(self):
        self.category_input.clear()
        self.amount_input.clear()

    def export_budget(self):
        selected_business = self.business_selector.currentText()
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Export Budget", "", "CSV Files (*.csv)")
        if selected_business and file_path:
            self.data_handler.save_budget(file_path, selected_business)

    def import_budget(self):
        selected_business = self.business_selector.currentText()
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Import Budget", "", "CSV Files (*.csv)")
        if selected_business and file_path:
            self.data_handler.load_budget(file_path, selected_business)
