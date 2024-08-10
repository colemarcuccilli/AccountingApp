from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMenuBar, QAction
from dashboard import Dashboard
from financial_statements import FinancialStatements
from data_entry import DataEntry
from business_management import BusinessManagement
from ledger import Ledger
from transactions import Transaction
from budget import Budget
from tax import Tax
from data_handler import DataHandler
from styles import styles

class AccountingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accounting App")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(styles["window"])
        self.businesses = {}
        self.data_handler = DataHandler(self.businesses)

        self.create_menu()
        self.tab_control = QTabWidget()
        self.setCentralWidget(self.tab_control)

        self.dashboard_tab = QWidget()
        self.business_management_tab = QWidget()
        self.financial_statements_tab = QWidget()
        self.data_entry_tab = QWidget()
        self.ledger_tab = QWidget()
        self.transaction_tab = QWidget()
        self.budget_tab = QWidget()
        self.tax_tab = QWidget()

        self.tab_control.addTab(self.dashboard_tab, "Dashboard")
        self.tab_control.addTab(self.business_management_tab, "Manage Businesses")
        self.tab_control.addTab(self.financial_statements_tab, "Financial Statements")
        self.tab_control.addTab(self.data_entry_tab, "Data Entry")
        self.tab_control.addTab(self.ledger_tab, "Ledger")
        self.tab_control.addTab(self.transaction_tab, "Transactions")
        self.tab_control.addTab(self.budget_tab, "Budget")
        self.tab_control.addTab(self.tax_tab, "Tax")

        self.setup_dashboard_tab()
        self.setup_business_management_tab()
        self.setup_financial_statements_tab()
        self.setup_data_entry_tab()
        self.setup_ledger_tab()
        self.setup_transaction_tab()
        self.setup_budget_tab()
        self.setup_tax_tab()

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)

        export_action = QAction('Export', self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv)")
        if file_path:
            self.data_handler.save_data(file_path)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "CSV Files (*.csv)")
        if file_path:
            self.data_handler.load_data(file_path)
            self.refresh_tabs()

    def export_data(self):
        selected_business = self.tab_control.currentWidget().business_selector.currentText()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv)")
        if selected_business and file_path:
            self.data_handler.save_ledger(file_path.replace(".csv", "_ledger.csv"), selected_business)
            self.data_handler.save_transactions(file_path.replace(".csv", "_transactions.csv"), selected_business)
            self.data_handler.save_budget(file_path.replace(".csv", "_budget.csv"), selected_business)
            self.data_handler.save_taxes(file_path.replace(".csv", "_taxes.csv"), selected_business)

    def setup_dashboard_tab(self):
        self.dashboard = Dashboard(self.dashboard_tab, self.businesses)

    def setup_business_management_tab(self):
        self.business_management = BusinessManagement(self.business_management_tab, self.businesses, self.dashboard.update_businesses, self.refresh_tabs)

    def setup_financial_statements_tab(self):
        self.financial_statements = FinancialStatements(self.financial_statements_tab, self.businesses)

    def setup_data_entry_tab(self):
        self.data_entry = DataEntry(self.data_entry_tab, self.businesses)

    def setup_ledger_tab(self):
        self.ledger = Ledger(self.ledger_tab, self.businesses)

    def setup_transaction_tab(self):
        self.transaction = Transaction(self.transaction_tab, self.businesses)

    def setup_budget_tab(self):
        self.budget = Budget(self.budget_tab, self.businesses)

    def setup_tax_tab(self):
        self.tax = Tax(self.tax_tab, self.businesses)

    def refresh_tabs(self):
        self.dashboard.update_businesses()
        self.business_management.update_businesses()
        self.financial_statements.update_businesses()
        self.data_entry.update_businesses()
        self.ledger.update_businesses()
        self.transaction.update_businesses()
        self.budget.update_businesses()
        self.tax.update_businesses()
