from datetime import datetime


def deal_year(widget):
    year_now = datetime.now().year
    widget.addItem(str(year_now))
    widget.addItem(str(year_now + 1))


def deal_month(widget):
    month_now = datetime.now().month
    for i in range(1, 13):
        widget.addItem(str(i))
    widget.setCurrentIndex(month_now - 1)


def deal_day(widget, month):
    month_text = month.currentText()
    widget.clear()
    day = 31
    if month_text in ["2", "4", "6", "9", "11"]:
        day = 30
    for i in range(1, day + 1):
        widget.addItem(str(i))


def deal_hour_from(widget):
    hour_now = datetime.now().hour
    for i in range(24):
        widget.addItem(str(i))
        widget.setCurrentIndex(hour_now)


def deal_hour_to(widget, hour_from):
    hour_from_text = int(hour_from.currentText())
    print(hour_from_text)
    widget.clear()
    for i in range(hour_from_text + 1, 50):
        if hour_from_text == 23:
            widget.addItem("00")
            return
        if i <= 23:
            widget.addItem(str(i))
        elif i == 24:
            widget.addItem("00")
        else:
            return
