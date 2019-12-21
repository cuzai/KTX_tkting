import time
import random

from Check_Chromedriver.Check_Chromedriver import Check_Chromedriver
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import login_info


class Tkting:
    def __init__(self, is_headless=False):
        cc = Check_Chromedriver()
        cc.main()

        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-infobars")
        if is_headless:
            self.chrome_options.add_argument("--headless")

        self.add_info = {
            "id": login_info.id,
            "pwd": login_info.pwd,
            "depart": "부산",
            "dest": "서울",
            "month": "12",
            "day": "22",
            "depart_time_from": "18",
            "depart_time_to": "19",
            "people": "1",
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

    def input_things(self, driver):
        driver.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")
        driver.implicitly_wait(10)

        # input departure
        self.input_departure(driver)

        # input month and day
        month_info = ["#s_month option", self.add_info["month"]]
        day_info = ["#s_day option", self.add_info["day"]]
        for info in [month_info, day_info]:
            self.input_month_day(driver, info[0], info[1])

        # input time and people
        time_info = ["#s_hour option", self.add_info["depart_time_from"]]
        people_info = ["#peop01 option", self.add_info["people"]]
        for info in [time_info, people_info]:
            self.input_time_people(driver, info[0], info[1])

        # submit
        self.submit(driver)

    def input_departure(self, driver):
        driver.find_element_by_css_selector("#start").clear()
        driver.find_element_by_css_selector("#get").clear()
        driver.find_element_by_css_selector("#start").send_keys(self.add_info["depart"])
        driver.find_element_by_css_selector("#get").send_keys(self.add_info["dest"])

    def input_month_day(self, driver, selector, info):
        # input month
        options = driver.find_elements_by_css_selector(selector)
        for op in options:
            if op.text == info:
                op.click()
                break

    def input_time_people(self, driver, selector, info):
        options = driver.find_elements_by_css_selector(selector)
        for op in options:
            if op.get_attribute("value") == info:
                op.click()
                break

    def submit(self, driver):
        driver.find_element_by_css_selector(".btn_inq").click()
        driver.implicitly_wait(10)

    def deal_alert(self, driver):
        try:
            text = driver.switch_to.alert.text
            print(text)
        except selenium.common.exceptions.NoAlertPresentException:
            pass

    def reservation(self, driver):
        idx = 0
        self.how_many_next = 0

        while True:
            tickets = driver.find_elements_by_css_selector("#tableResult tbody tr")
            for ticket in tickets:
                print(idx, ", ", end="")
                idx += 1

                # time
                raw_daprt_time = ticket.find_elements_by_css_selector("td")[2].text

                normal_seat = ticket.find_elements_by_css_selector("td")[5]
                isAvailable = normal_seat.find_element_by_css_selector(
                    "img"
                ).get_attribute("alt")
                if isAvailable == "예약하기":
                    normal_seat.find_element_by_css_selector("img").click()
                    print("Got it")
                    return True
            self.deal_btns(driver)

    def deal_btns(self, driver):
        next_btn = driver.find_elements_by_css_selector("table.btn img")[-1]
        if next_btn.get_attribute("alt") == "다음":
            next_btn.click()
            self.how_many_next += 1
            print("next")
            time.sleep(random.randint(1, 3))
            return
        self.submit(driver)
        print("first")

    def main(self):
        driver = self.get_driver()
        try:
            self.login(driver)
            self.input_things(driver)
            self.deal_alert(driver)
            self.reservation(driver)
        finally:
            time.sleep(60)
            driver.quit()
            print("killed")


if __name__ == "__main__":
    Tkting().main()
