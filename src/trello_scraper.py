import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_board_json(driver, config):

    driver.get('https://trello.com')

    wait = WebDriverWait(driver, timeout=10)

    # login button
    log_in_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@data-uuid="MJFtCCgVhXrVl7v9HA7EH_login"]'))
    )
    log_in_btn.click()

    # email field
    email_txt_field = driver.find_element(By.ID, "username")
    wait.until(lambda _: email_txt_field.is_displayed())
    email_txt_field.send_keys(config.email)

    # continue button
    continue_btn = driver.find_element(By.ID, "login-submit")
    wait.until(lambda _: continue_btn.is_displayed())
    continue_btn.click()

    # wait for password field and login
    pw_txt_field = driver.find_element(By.ID, "password")
    wait.until(lambda _: pw_txt_field.is_displayed())
    pw_txt_field.send_keys(config.password, Keys.ENTER)

    driver.implicitly_wait(5)

    # wait for boards to load
    content_div = driver.find_element(By.ID, "content")
    wait.until(lambda _: content_div.is_displayed())

    driver.get(config.board_url + ".json")

    raw_data_btn = wait.until(
        EC.presence_of_element_located((By.ID, "rawdata-tab")))
    raw_data_btn.click()
    raw_data_pre = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'pre.data')))
    raw_json = raw_data_pre.text

    board_json = json.loads(raw_json)

    driver.quit()

    return board_json
