import time
import re

from Check_Chromedriver import Check_Chromedriver as cc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import login_info
from PyQt5.QtCore import QThread

from libs import Deal_btns, Input_things, Deal_alert


class Tkting(Qthread):
    alert = pyqtSignal(str)

    def __init__(self, is_headless=False):
        cc.main()

        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        if is_headless:
            self.chrome_options.add_argument("--headless")

        self.add_info = {
            "id": login_info.id,
            "pwd": login_info.pwd,
            "depart": "서울",
            "dest": "부산",
            "year": "2019",
            "month": "12",
            "day": "25",
            "depart_time_from": "18",
            "depart_time_to": "24",
            "people": "1",
            "train": "KTX",
            "card_num": login_info.card_num,
            "card_month": login_info.card_month,
            "card_year": login_info.card_year,
            "card_pwd": login_info.card_pwd,
            "identity": login_info.identity,
        }

    def get_driver(self):
        driver = webdriver.Chrome(
            executable_path="chromedriver/chromedriver.exe",
            chrome_options=self.chrome_options,
        )
        return driver

    def login(self, driver):
        driver.get("http://www.letskorail.com/korail/com/login.do")
        driver.implicitly_wait(10)
        driver.find_element_by_css_selector("#txtMember").send_keys(self.add_info["id"])
        driver.find_element_by_css_selector("#txtPwd").send_keys(self.add_info["pwd"])
        driver.find_element_by_css_selector(".btn_login").click()

    def reservation(self, driver):
        idx = 0

        while True:
            tickets = driver.find_elements_by_css_selector("#tableResult tbody tr")
            go_next = True
            for ticket in tickets:
                # time
                raw_daprt_time = ticket.find_elements_by_css_selector("td")[2].text
                p = re.compile(".*\n(.*):.*")
                m = p.search(raw_daprt_time)
                depart_time = m.group(1)

                if depart_time > self.add_info["depart_time_to"]:
                    Deal_btns.submit(driver)
                    go_next = False
                    break
                if self.add_info["train"] != "":
                    # train
                    train = ticket.find_elements_by_css_selector("td")[1].get_attribute(
                        "title"
                    )
                    if train != self.add_info["train"]:
                        continue

                normal_seat = ticket.find_elements_by_css_selector("td")[5]
                isAvailable = normal_seat.find_element_by_css_selector(
                    "img"
                ).get_attribute("alt")
                if isAvailable == "예약하기":
                    normal_seat.find_element_by_css_selector("img").click()
                    print("Got it")
                    driver.implicitly_wait(10)
                    return True
                print("{}. {} - {}".format(idx, train, depart_time))
                idx += 1

            if go_next:
                Deal_btns.next_btns(driver)

    def payment(self, driver):
        # card info
        input_card_info = driver.find_elements_by_css_selector(
            "#Div_Card tbody.lef tr"
        )[1].find_elements_by_css_selector("input")

        card_num = self.add_info["card_num"].split("-")

        # input card num
        for n, i in enumerate(input_card_info):
            i.send_keys(card_num[n])

        # input card month
        month_ops = driver.find_elements_by_css_selector("#month option")
        for op in month_ops:
            if op.text == self.add_info["card_month"]:
                op.click()

        # input card year
        year_ops = driver.find_elements_by_css_selector("#year option")
        for op in year_ops:
            if op.text == self.add_info["card_year"]:
                op.click()

        # input card pwd
        input_card_pwd = driver.find_elements_by_css_selector("#Div_Card tbody.lef tr")[
            4
        ].find_element_by_css_selector("input")
        input_card_pwd.send_keys(self.add_info["card_pwd"])

        # input 주민번호
        identity_info = driver.find_elements_by_css_selector("#Div_Card tbody.lef tr")[
            5
        ].find_element_by_css_selector("input")
        identity_info.send_keys(self.add_info["identity"])

        # check checkbox
        driver.find_element_by_css_selector("#chkAgree").click()

        driver.find_element_by_css_selector("#fnIssuing").click()

        # click the last button
        driver.implicitly_wait(10)
        driver.find_element_by_css_selector("#tabSale3").click()
        driver.implicitly_wait(10)
        time.sleep(5)

        driver.switch_to.frame("mainframeSaleInfo")
        driver.find_element_by_css_selector("#radSmart1").click()
        driver.find_element_by_css_selector("#btn_next").click()
        Deal_alert.print_alert_all(driver)

    def run(self):
        driver = self.get_driver()
        try:
            self.login(driver)
            Input_things.input_things(driver, self.add_info)
            Deal_alert.print_alert_all(driver)
            if self.reservation(driver):
                Deal_alert.print_alert_all(driver)
                driver.find_element_by_css_selector("#btn_next").click()
                self.payment(driver)
        finally:
            # time.sleep(60)
            driver.quit()
            print(
                "-----------------------------killed---------------------------------"
            )


if __name__ == "__main__":
    Tkting().main()
