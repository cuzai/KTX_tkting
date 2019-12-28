import sys
from functools import partial
from datetime import datetime
import re


from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSlot

# from ui.myUi import Ui_MainWindow

from lib_for_QT.login_dialog import Login_dialog
from lib_for_QT import date_init
from tkting import Tkting

form_class = uic.loadUiType("./ui/untitled.ui")[0]


# class Main(QtWidgets.QMainWindow, Ui_MainWindow) :
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
        print(self.combo_year.currentText())
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
        try:
            if (
                len(self.add_info) >= 11
                and self.combo_destination.currentText() != "--선택--"
                and self.combo_departure.currentText() != "--선택--"
            ):
                self.status.setText("티켓을 찾는 중...")
                tkting = Tkting()
                tkting.add_info = self.add_info
                tkting.run()
        except Exception as e:
            m = re.compile("Alert Text: (.*)\n.*")
            p = m.search(str(e))
            try:
                self.status.setText(p.group(1))
            except AttributeError:
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
