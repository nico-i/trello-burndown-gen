import argparse
import json
import logging
import os
from datetime import date, timedelta

import coloredlogs
import verboselogs

from src.board_parser import parse_board
from src.config_parser import get_config, get_driver
from src.data_processor import create_df
from src.plotter import plot_burn_down
from src.trello_scraper import get_board_json
from src.util.constants import CACHE_FILE_NAME, CONFIG_FILE_NAME, DATE_FORMAT
from src.util.helper import valid_date


def main():
    verboselogs.install()
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    logger.notice('+++ Welcome to Trello Burn-down! +++')
    logger.verbose('Use -h or --help for help')
    logger.notice('--- Starting program ---')
    parser = argparse.ArgumentParser(prog='Trello Burn-down Generator',
                                     description="Create a plot from a Trello board's JSON data!")

    current_dir_path = os.path.dirname(
        os.path.abspath(__file__))
    config_file_path = os.path.join(
        current_dir_path, CONFIG_FILE_NAME)

    parser.add_argument("--config", "-c", type=str, default=config_file_path,
                        help="path to config file [default: %s]" % config_file_path)

    parser.add_argument("--browser", "-b", type=str,
                        help="browser driver to run selenium in [default: None]")
    parser.add_argument("--headless", "-hl", action="store_true", default=False,
                        help="run selenium in headless mode [default: None]")
    # --refetch or -r, store_true means it does not accept any value, if present it's True else False
    parser.add_argument("--refetch", "-r", action="store_true", default=False,
                        help="refetches board data from Trello when present [default: None]")
    parser.add_argument("--email", "-em", type=str,
                        help="email address of your Trello account [default: None]")
    parser.add_argument("--password", "-p", type=str,
                        help="password of your Trello account [default: None]")
    parser.add_argument("--board", "-bo", type=str,
                        help="URL of the Trello board [default: None]")
    parser.add_argument("--member", "-m", type=str,
                        help="name of the Trello member for which to create an individual burn-down chart (optional) [default: None]")
    parser.add_argument("--resolved", "-re", type=str,
                        help="name of the resolved list [default: None]")
    parser.add_argument("--sprint", "-sp", type=str,
                        help="name of the sprint backlog list [default: None]")

    today_str = date.today().strftime(DATE_FORMAT)
    parser.add_argument("--end", "-e", type=valid_date,
                        help="end date of the sprint in DD.MM.YY format [default: today i. e. %s)" % today_str, default=today_str)

    parser.add_argument("--duration", "-d", type=int, default=14,
                        help="duration of the sprint in days [default value: 14)")
    args = parser.parse_args()
    args_dict = vars(args)

    config = get_config(logger, args_dict)

    logger.info("Creating burn-down chart for sprint %s - %s" %
                (config.start_date.strftime(DATE_FORMAT), config.end_date.strftime(DATE_FORMAT)))

    logger.verbose("Retrieving board data...")

    if args.refetch:
        # delete cache file
        logger.info("--refetch enabled. Removing board cache...")
        os.remove(CACHE_FILE_NAME)

    if os.path.exists(CACHE_FILE_NAME):
        logger.info("--refetch disabled. Using cached board data...")
        with open(CACHE_FILE_NAME, 'r', encoding="utf8") as f:
            # Load the JSON content
            board_json = json.load(f)
    else:
        logger.info("No cached board data found. Refetching board data...")
        driver = get_driver(config=config)
        board_json = get_board_json(driver, config)
        with open(CACHE_FILE_NAME, 'w') as f:
            json.dump(board_json, f, indent=4)

    logger.info("Board data retrieved successfully!")
    _, _, board_cards = parse_board(logger,
                                    config, board_json)

    df = create_df(logger, config,
                   board_cards)

    plot_burn_down(logger, df)


if __name__ == "__main__":
    main()
