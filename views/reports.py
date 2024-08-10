from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from styles import styles

class Reports(QWidget):
    def __init__(self, parent, businesses):
        super().__init__(parent)
        self.businesses = businesses
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        label = QLabel("Reports")
        label.setStyleSheet(styles["header"])
        layout.addWidget(label)

        self.business_selector = QComboBox()
        self.update_businesses()
        layout.addWidget(self.business_selector)

        generate_report_button = QPushButton("Generate Report")
        generate_report_button.setStyleSheet(styles["button"])
        generate_report_button.clicked.connect(self.generate_report)
        layout.addWidget(generate_report_button)

        self.setLayout(layout)

    def update_businesses(self):
        self.business_selector.clear()
        self.business_selector.addItems(self.businesses.keys())

    def generate_report(self):
        selected_business = self.business_selector.currentText()
        if selected_business:
            # Logic to generate and display reports for the selected business
            pass
