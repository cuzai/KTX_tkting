from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


form_class = uic.loadUiType("./ui/login.ui")[0]


class Login_dialog(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.pushButtonClicked)

    def pushButtonClicked(self):
        self.id = self.lineEdit.text()
        self.password = self.lineEdit_2.text()
        if self.id == "" or self.password == "":
            return
        self.close()
