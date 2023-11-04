import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as Options_firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from util.constants import CONFIG_FILE_NAME
from util.models import Browser, Config


def get_config(logger):

    logger.verbose("Loading config from %s..." % CONFIG_FILE_NAME)
    current_dir_path = os.path.dirname(
        os.path.abspath(__file__))

    config_file_path = os.path.join(current_dir_path, '..', CONFIG_FILE_NAME)

    # use utf 8
    with open(config_file_path, 'r', encoding="utf8") as f:
        config_json_data = json.load(f)

    config = Config(config_json_data['browser'], config_json_data['headless'], config_json_data['email'], config_json_data['password'],
                    config_json_data['board_url'], config_json_data['sprint_bl_list_name'], config_json_data['resolved_list_name'])

    if(config_json_data['member_name'] is not None):
        config.member_name = config_json_data['member_name']

    logger.info("Config loaded successfully!")
    logger.verbose("Browser: '%s'" % config.browser)
    logger.verbose("Headless mode: %s" % config.headless)
    logger.verbose("Trello board URL: '%s'" % config.board_url)
    if(config.member_name is not None):
        logger.verbose("Member: '%s'" % config.member_name)
    else:
        logger.verbose("Member: N/A")
    logger.verbose("Resolved list name: '%s'" % config.resolved_list_name)
    logger.verbose("Sprint backlog list name: '%s'" %
                   config.sprint_bl_list_name)
    logger.verbose("Trello username: '%s'" % config.email)
    logger.verbose("Trello password: %s" % ("*" * len(config.password)))

    return config


def get_driver(config):
    driver = None
    options = None

    if (config.browser == Browser.FIREFOX.value):
        options = Options_firefox()
        if (config.headless):
            options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=options)
    elif (config.browser == Browser.CHROME.value):
        options = Options_chrome()
        if (config.headless):
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--None")
        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()), options=options)

    if (driver is None):
        raise ValueError("Selenium browser could not be initialized!")

    return driver
