import sys
from functools import partial
from datetime import datetime
import re

import PyQt5
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

# from ui.myUi import Ui_MainWindow

from lib_for_QT.login_dialog import Login_dialog
from lib_for_QT import date_init
from tkting import Tkting

form_class = uic.loadUiType("./ui/untitled.ui")[0]


# class Main(QtWidgets.QMainWindow, Ui_MainWindow) :
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Main(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        self.removed_station_name = ""
        self.removed_station_index = 0
        super().__init__()

        self.add_info = {}

        self.login()

        self.setupUi(self)

        self.radio_init()

        # date init
        date_init.deal_year(self.combo_year)
        date_init.deal_month(self.combo_month)
        self.combo_month.currentIndexChanged.connect(
            partial(date_init.deal_day, self.combo_day, self.combo_month)
        )

        date_init.deal_day(self.combo_day, self.combo_month)
        day_now = datetime.now().day
        self.combo_day.setCurrentIndex(day_now - 1)

        date_init.deal_hour_from(self.combo_hour_from)
        self.combo_hour_from.currentIndexChanged.connect(
            partial(date_init.deal_hour_to, self.combo_hour_to, self.combo_hour_from)
        )

        date_init.deal_hour_to(self.combo_hour_to, self.combo_hour_from)

        date_li = [
            self.combo_year,
            self.combo_month,
            self.combo_day,
            self.combo_hour_from,
            self.combo_hour_to,
        ]
        for date in date_li:
            date.currentIndexChanged.connect(self.deal_combo)

        self.station_init()

        self.person_init()

        self.button_init()

    @pyqtSlot()
    def login(self):
        dlg = Login_dialog()
        dlg.exec_()
        self.add_info["id"] = dlg.id
        self.add_info["pwd"] = dlg.password

    def radio_init(self):
        self.radio_ktx.setChecked(True)
        car_li = [self.radio_all, self.radio_ktx, self.radio_flower]
        for car in car_li:
            car.clicked.connect(partial(self.deal_radio, car_li, "train"))
        self.deal_radio(car_li, "train")

    def station_init(self):
        station_li = [
            "--선택--",
            "서울",
            "인청공항T1",
            "천안아산",
            "대전",
            "서대전",
            "동대구",
            "포항",
            "신경주",
            "울산(통도사)",
            "부산",
            "마산",
            "창원",
            "창원중앙",
            "전주",
            "목포",
        ]
        for station in station_li:
            self.combo_departure.addItem(station)
            self.combo_destination.addItem(station)

        for i in [self.combo_departure, self.combo_destination]:
            i.currentIndexChanged.connect(self.deal_combo)
        self.combo_departure.currentIndexChanged.connect(self.deal_station)

    def deal_station(self):
        if self.removed_station_name != "":
            self.combo_destination.insertItem(
                self.removed_station_index, self.removed_station_name
            )
        self.removed_station_name = self.combo_departure.currentText()
        self.removed_station_index = self.combo_departure.currentIndex()
        self.combo_destination.removeItem(self.combo_departure.currentIndex())

    def person_init(self):
        for i in range(1, 6):
            self.combo_person.addItem(str(i))
        self.combo_person.currentIndexChanged.connect(self.deal_combo)

    def button_init(self):
        self.pushButton.clicked.connect(self.click_button)

    def deal_radio(self, radio_li, info):
        for radio in radio_li:
            if radio.isChecked():
                text = radio.text()
                if text == "전체":
                    text = ""

                elif text == "KTX/KTX-산천":
                    text = "KTX"

                self.add_info[info] = text
                return

    def deal_combo(self):
        self.add_info["year"] = self.combo_year.currentText()
        self.add_info["month"] = self.combo_month.currentText()
        self.add_info["day"] = self.combo_day.currentText()
        self.add_info["depart_time_from"] = self.combo_hour_from.currentText()
        self.add_info["depart_time_to"] = self.combo_hour_to.currentText()
        self.add_info["depart"] = self.combo_departure.currentText()
        self.add_info["dest"] = self.combo_destination.currentText()
        self.add_info["people"] = self.combo_person.currentText()

    def click_button(self):
        if (
            len(self.add_info) >= 11
            and self.combo_destination.currentText() != "--선택--"
            and self.combo_departure.currentText() != "--선택--"
        ):
            self.tkt = Tkting()
            self.tkt.add_info = self.add_info
            self.status.setText("티켓을 찾는 중...")
            self.tkt.alert.connect(self.setStatus)
            self.tkt.error.connect(self.setError)
            self.tkt.start()
            self.pushButton.setEnabled(False)

    @pyqtSlot(str, list)
    def setStatus(self, e, driver):
        self.status.setText(e)
        driver[0].quit()
        print("setstatus")

    @pyqtSlot(str)
    def setError(self, e):
        try:
            m = re.compile("Alert Text: (.*)\n.*")
            p = m.search(str(e))
            self.status.setText(p.group(1))
            print("seterror")
            if p.group(1) == "회원번호를 정확하게 입력하여 주십시오.":
                self.label_id = QtWidgets.QLabel(self.groupBox_6)
                self.label_id.setAlignment(
                    QtCore.Qt.AlignRight
                    | QtCore.Qt.AlignTrailing
                    | QtCore.Qt.AlignVCenter
                )
                self.label_id.setObjectName("label_id")
                self.gridLayout_11.addWidget(self.label_id, 0, 1)
                self.label_id.setText("ID(회원번호) ")

                self.label_pwd = QtWidgets.QLabel(self.groupBox_6)
                self.label_pwd.setAlignment(
                    QtCore.Qt.AlignRight
                    | QtCore.Qt.AlignTrailing
                    | QtCore.Qt.AlignVCenter
                )
                self.label_pwd.setObjectName("label_pwd")
                self.gridLayout_11.addWidget(self.label_pwd, 0, 3)
                self.label_pwd.setText("비밀번호 ")

                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
                )
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)

                self.lineEdit_pwd = QtWidgets.QLineEdit(self.groupBox_6)
                sizePolicy.setHeightForWidth(
                    self.lineEdit_pwd.sizePolicy().hasHeightForWidth()
                )

                self.lineEdit_pwd.setSizePolicy(sizePolicy)
                self.lineEdit_pwd.setObjectName("lineEdit_pwd")
                self.gridLayout_11.addWidget(self.lineEdit_pwd, 0, 4)
                self.lineEdit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)

                self.lineEdit_id = QtWidgets.QLineEdit(self.groupBox_6)
                sizePolicy.setHeightForWidth(
                    self.lineEdit_id.sizePolicy().hasHeightForWidth()
                )
                self.lineEdit_id.setSizePolicy(sizePolicy)
                self.lineEdit_id.setObjectName("lineEdit_id")
                self.gridLayout_11.addWidget(self.lineEdit_id, 0, 2)

                self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_4)
                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
                )
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(
                    self.pushButton_2.sizePolicy().hasHeightForWidth()
                )
                self.pushButton_2.setSizePolicy(sizePolicy)
                self.pushButton_2.setObjectName("pushButton_2")
                self.gridLayout_10.addWidget(self.pushButton_2, 0, 5)
                self.pushButton_2.setText("로그인")
                self.pushButton_2.clicked.connect(self.login_again)

                self.pushButton.setEnabled(True)

        except AttributeError:
            print("serterror2")
            self.status.setText("")
            self.pushButton.setEnabled(True)
            pass

    def login_again(self):
        new_id = self.lineEdit_id.text()
        self.add_info["id"] = new_id
        self.add_info["pwd"] = self.lineEdit_pwd.text()
        # print(self.add_info)
        self.pushButton_2.setEnabled(False)
        self.label_id.setEnabled(False)
        self.lineEdit_id.setEnabled(False)
        self.lineEdit_pwd.setEnabled(False)
        self.label_pwd.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
