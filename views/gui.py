import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from views.dashboard import Dashboard
from views.business_management import BusinessManagement
from views.data_entry import DataEntry
from views.ledger import Ledger
from views.transactions import Transactions
from views.reports import Reports
from views.data_handler import DataHandler

class AccountingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accounting App")
        self.setGeometry(100, 100, 800, 600)

        self.data_handler = DataHandler()
        self.businesses = self.data_handler.load_data()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.dashboard = Dashboard(self, self.businesses)
        self.business_management = BusinessManagement(self, self.businesses, self.refresh_tabs)
        self.data_entry = DataEntry(self, self.businesses)
        self.ledger = Ledger(self, self.businesses)
        self.transactions = Transactions(self, self.businesses)
        self.reports = Reports(self, self.businesses)

        self.tab_widget.addTab(self.dashboard, "Dashboard")
        self.tab_widget.addTab(self.business_management, "Business Management")
        self.tab_widget.addTab(self.data_entry, "Data Entry")
        self.tab_widget.addTab(self.ledger, "Ledger")
        self.tab_widget.addTab(self.transactions, "Transactions")
        self.tab_widget.addTab(self.reports, "Reports")

    def refresh_tabs(self):
        self.dashboard.update_dashboard()
        self.data_entry.update_account_dropdowns(self.data_entry.business_selector.currentText())
        self.ledger.update_ledger(self.ledger.business_selector.currentText())

def main():
    app = QApplication(sys.argv)
    window = AccountingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
