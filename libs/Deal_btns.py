import random
import time


def next_btns(driver):
    next_btn = driver.find_elements_by_css_selector("table.btn img")[-1]
    if next_btn.get_attribute("alt") == "다음":
        next_btn.click()
        print("next")
        time.sleep(random.randint(1, 3))
        return
    submit(driver)
    return


def submit(driver):
    driver.find_element_by_css_selector(".btn_inq").click()
    print("refresh")
    time.sleep(random.randint(1, 3))
    return
