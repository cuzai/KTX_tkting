import selenium
import time


def print_alert(driver):
    try:
        text = driver.switch_to.alert.text
        print(text)
    except selenium.common.exceptions.NoAlertPresentException:
        pass


def deal_alert_all(driver):
    try:
        while True:
            driver.switch_to.alert.accept()
            time.sleep(1)
    except selenium.common.exceptions.NoAlertPresentException:
        pass


def print_alert_all(driver, signal):
    text_li = []
    try:
        while True:
            text = driver.switch_to.alert.text
            driver.switch_to.alert.accept()
            signal.emit(text, [driver])
            time.sleep(1)
    except selenium.common.exceptions.NoAlertPresentException:
        return text_li
