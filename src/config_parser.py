import datetime
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as Options_firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.util.constants import CONFIG_FILE_NAME, DATE_FORMAT
from src.util.models import Browser, Config


def get_config(logger, args_dict):
    config_file_path = args_dict["config"]

    if os.path.isfile(config_file_path) == False:
        # check if all args (except optional 'member') are set in case of config not existing
        for key, value in args_dict.items():
            if key == "member":
                continue
            if value == None:
                raise ValueError(
                    "'%s' is None! Either a config file or all required arguments must be provided!"
                    % key
                )
        logger.verbose("No config file present, creating config from arguments...")
        config = Config(
            browser=args_dict.browser,
            headless=args_dict.headless,
            refetch=args_dict.refetch,
            email=args_dict.email,
            password=args_dict.password,
            board_url=args_dict.board,
            sprint_bl_list_name=args_dict.sprint,
            resolved_list_name=args_dict.resolved,
            end_date=args_dict.end,
            duration=args_dict.duration,
            member_name=args_dict.member,
        )
    else:
        logger.verbose("Loading config from '%s' ..." % config_file_path)

        with open(config_file_path, "r", encoding="utf8") as f:
            config_json_data = json.load(f)

        for key in args_dict.keys():
            if key == "member" or key == "config":
                continue
            try:
                config_json_data[key]
            except KeyError:
                if args_dict[key] == None:
                    raise ValueError(
                        "Value '%s' must be set in either the config or as an argument!"
                        % key
                    )
                else:
                    config_json_data[key] = args_dict[key]
        config = Config(
            browser=config_json_data["browser"],
            headless=config_json_data["headless"],
            refetch=config_json_data["refetch"],
            email=config_json_data["email"],
            password=config_json_data["password"],
            board_url=config_json_data["board_url"],
            sprint_bl_list_name=config_json_data["sprint_bl_name"],
            resolved_list_name=config_json_data["resolved_list_name"],
            end_date=config_json_data["sprint_end_date"],
            duration=int(config_json_data["sprint_duration"]),
            member_name=config_json_data["member"],
        )

    for key, value in args_dict.items():
        if value != None:
            setattr(config, key, value)
            logger.verbose(
                "Overriding config value '%s' with argument value '%s'" % (key, value)
            )
    logger.info("Config loaded successfully!")
    logger.verbose("Browser: '%s'" % config.browser)
    logger.verbose("Headless mode: %s" % config.headless)
    logger.verbose("Refetch: %s" % config.refetch)
    logger.verbose("Trello board URL: '%s'" % config.board_url)
    if config.member_name is not None:
        logger.verbose("Member: '%s'" % config.member_name)
    else:
        logger.verbose("Member: N/A")
    logger.verbose("Resolved list name: '%s'" % config.resolved_list_name)
    logger.verbose("Sprint backlog list name: '%s'" % config.sprint_bl_list_name)
    logger.verbose("Trello username: '%s'" % config.email)
    logger.verbose("Trello password: %s" % ("*" * len(config.password)))
    logger.verbose("Sprint start date: %s" % config.start_date.strftime("%d.%m.%Y"))
    logger.verbose("Sprint duration: %s days" % config.duration)
    logger.verbose("Sprint end date: %s" % config.end_date.strftime("%d.%m.%Y"))
    return config


def get_driver(config):
    driver = None
    options = None

    if config.browser == Browser.FIREFOX.value:
        options = Options_firefox()
        if config.headless:
            options.headless = True
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
    elif config.browser == Browser.CHROME.value:
        options = Options_chrome()
        if config.headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--None")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    if driver is None:
        raise ValueError("Selenium browser could not be initialized!")

    return driver
