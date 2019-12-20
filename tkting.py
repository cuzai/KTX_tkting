from Check_Chromedriver.Check_Chromedriver import Check_Chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import login_info


class Tkting:
    def __init__(self, is_headless=False):
        cc = Check_Chromedriver()
        cc.main()

        self.chrome_options = Options()
        if is_headless:
            self.chrome_options.add_argument("--headless")

        # id = login_info.id
        # pwd = login_info.pwd

    def get_driver(self):
        driver = webdriver.Chrome(
            executable_path="chromedriver/chromedriver.exe",
            chrome_options=self.chrome_options,
        )
        return driver

    def login(self, driver):
        driver.get("http://www.letskorail.com/korail/com/login.do")
        driver.implicitly_wait(10)
        driver.find_element_by_css_selector("#txtMember").send_keys(login_info.id)
        driver.find_element_by_css_selector("#txtPwd").send_keys(login_info.pwd)
        driver.find_element_by_css_selector(".btn_login").click()

    def main(self):
        driver = self.get_driver()
        try:
            self.login(driver)
        finally:
            driver.quit()


if __name__ == "__main__":
    Tkting().main()

