from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton
import pandas as pd
from views.styles import styles

class Export:
    def __init__(self, parent, businesses):
        self.parent = parent
        self.businesses = businesses
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Export Financial Documents")
        label.setStyleSheet(styles["header"])
        layout.addWidget(label)

        self.business_selector = QComboBox()
        self.update_businesses()
        layout.addWidget(self.business_selector)

        export_balance_sheet_button = QPushButton("Export Balance Sheet")
        export_balance_sheet_button.setStyleSheet(styles["button"])
        export_balance_sheet_button.clicked.connect(self.export_balance_sheet)
        layout.addWidget(export_balance_sheet_button)

        export_income_statement_button = QPushButton("Export Income Statement")
        export_income_statement_button.setStyleSheet(styles["button"])
        export_income_statement_button.clicked.connect(self.export_income_statement)
        layout.addWidget(export_income_statement_button)

        export_cash_flow_button = QPushButton("Export Cash Flow Statement")
        export_cash_flow_button.setStyleSheet(styles["button"])
        export_cash_flow_button.clicked.connect(self.export_cash_flow_statement)
        layout.addWidget(export_cash_flow_button)

        self.parent.setLayout(layout)

    def update_businesses(self):
        self.business_selector.clear()
        self.business_selector.addItems(self.businesses.keys())

    def export_balance_sheet(self):
        selected_business = self.business_selector.currentText()
        if selected_business:
            # Create a sample DataFrame
            data = {
                "Category": ["Assets", "Liabilities", "Equity"],
                "Amount": [10000, 5000, 5000]
            }
            df = pd.DataFrame(data)
            # Save the DataFrame to a CSV file
            file_path = f"{selected_business}_balance_sheet.csv"
            df.to_csv(file_path, index=False)
            print(f"Balance sheet saved to {file_path}")

    def export_income_statement(self):
        selected_business = self.business_selector.currentText()
        if selected_business:
            # Logic to export income statement
            print(f"Exporting Income Statement for {selected_business}")

    def export_cash_flow_statement(self):
        selected_business = self.business_selector.currentText()
        if selected_business:
            # Logic to export cash flow statement
            print(f"Exporting Cash Flow Statement for {selected_business}")
