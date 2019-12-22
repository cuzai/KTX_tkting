from libs import Deal_btns


def input_things(driver, add_info):
    driver.get("http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")
    driver.implicitly_wait(10)

    # input departure
    input_departure(driver, add_info)

    # input month and day
    month_info = ["#s_month option", add_info["month"]]
    day_info = ["#s_day option", add_info["day"]]
    for info in [month_info, day_info]:
        input_month_day(driver, info[0], info[1])

    # input time and people
    time_info = ["#s_hour option", add_info["depart_time_from"]]
    people_info = ["#peop01 option", add_info["people"]]
    for info in [time_info, people_info]:
        input_time_people(driver, info[0], info[1])

    # submit
    Deal_btns.submit(driver)


def input_departure(driver, add_info):
    driver.find_element_by_css_selector("#start").clear()
    driver.find_element_by_css_selector("#get").clear()
    driver.find_element_by_css_selector("#start").send_keys(add_info["depart"])
    driver.find_element_by_css_selector("#get").send_keys(add_info["dest"])


def input_month_day(driver, selector, info):
    # input month
    options = driver.find_elements_by_css_selector(selector)
    for op in options:
        if op.text == info:
            op.click()
            break


def input_time_people(driver, selector, info):
    options = driver.find_elements_by_css_selector(selector)
    for op in options:
        if op.get_attribute("value") == info:
            op.click()
            break
