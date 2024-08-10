from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from styles import styles

class Ledger(QWidget):
    def __init__(self, parent, businesses):
        super().__init__(parent)
        self.businesses = businesses
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Ledger")
        title.setStyleSheet(styles["header"])
        title.setFont(QFont('Arial', 24))
        layout.addWidget(title)

        self.business_selector = QComboBox()
        self.business_selector.addItems(self.businesses.keys())
        self.business_selector.currentTextChanged.connect(self.update_ledger)
        layout.addWidget(self.business_selector)

        self.ledger_table = QTableWidget()
        self.ledger_table.setColumnCount(5)
        self.ledger_table.setHorizontalHeaderLabels(["Date", "Description", "Debit Account", "Credit Account", "Amount"])
        layout.addWidget(self.ledger_table)

        self.setLayout(layout)
        self.update_ledger(self.business_selector.currentText())

    def update_ledger(self, business_name):
        self.ledger_table.setRowCount(0)
        if business_name in self.businesses:
            transactions = self.businesses[business_name]["transactions"]
            for transaction in transactions:
                row_position = self.ledger_table.rowCount()
                self.ledger_table.insertRow(row_position)
                self.ledger_table.setItem(row_position, 0, QTableWidgetItem(transaction["date"]))
                self.ledger_table.setItem(row_position, 1, QTableWidgetItem(transaction["description"]))
                self.ledger_table.setItem(row_position, 2, QTableWidgetItem(transaction["debit_account"]))
                self.ledger_table.setItem(row_position, 3, QTableWidgetItem(transaction["credit_account"]))
                self.ledger_table.setItem(row_position, 4, QTableWidgetItem(transaction["amount"]))
