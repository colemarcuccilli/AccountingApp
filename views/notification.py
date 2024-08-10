from PyQt5.QtWidgets import QMessageBox

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent

    def show_message(self, title, message):
        msg_box = QMessageBox(self.parent)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
