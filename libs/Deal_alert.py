import selenium


def deal_alert(driver):
    try:
        text = driver.switch_to.alert.text
        print(text)
    except selenium.common.exceptions.NoAlertPresentException:
        pass
