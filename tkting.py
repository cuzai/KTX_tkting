import re

from Check_Chromedriver.Check_Chromedriver import Check_Chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import login_info

from libs import Deal_btns, Input_things, Deal_alert


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
            "depart_time_to": "24",
            "people": "1",
            "train": "무궁화호",
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
                if isAvailable == "예약하기d":
                    normal_seat.find_element_by_css_selector("img").click()
                    print("Got it")
                    return True
                print("{}. {} - {}".format(idx, train, depart_time))
                idx += 1

            if go_next:
                Deal_btns.next_btns(driver)

    def main(self):
        driver = self.get_driver()
        try:
            self.login(driver)
            Input_things.input_things(driver, self.add_info)
            Deal_alert.deal_alert(driver)
            self.reservation(driver)
        finally:
            # time.sleep(60)
            driver.quit()
            print(
                "-----------------------------killed---------------------------------"
            )


if __name__ == "__main__":
    Tkting().main()
