import argparse
import json
import logging
import os
from datetime import date, datetime, timedelta

import coloredlogs
import verboselogs

from board_parser import parse_board
from config_parser import get_config, get_driver
from plotter import plot_burndown
from trello_scraper import get_board_json
from util.constants import CACHE_FILE_NAME, DATE_FORMAT


def main():
    verboselogs.install()
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    logger.notice('+++ Welcome to Trello Burndown! +++')
    logger.verbose('Use -h or --help for help')
    logger.notice('--- Starting program ---')
    parser = argparse.ArgumentParser(prog='burndown_gen.py',
                                     description='Trello Burndown Generator: Create a plot from a Trello board\'s JSON data!')

    # --refetch or -r, store_true means it does not accept any value, if present it's True else False
    parser.add_argument("--refetch", "-r", action="store_true",
                        help="refetches board data from Trello when present")
    # --end <date> or -e <date>
    today_str = date.today().strftime(DATE_FORMAT)
    parser.add_argument("--end", "-e", type=valid_date,
                        help="end date of the sprint in DD.MM.YY format (default: today i. e. %s)" % today_str, default=today_str)
    # --duration <days> or -d <days>
    parser.add_argument("--duration", "-d", type=int,
                        help="duration of the sprint in days (default value: 14)", default=14)

    args = parser.parse_args()

    end_date = args.end
    start_date = end_date - timedelta(days=args.duration)

    logger.info("Creating burndown chart for sprint %s - %s" %
                (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT)))

    config = get_config(logger)

    logger.verbose("Retrieving board data...")

    if os.path.exists(CACHE_FILE_NAME) and not args.refetch:
        logger.info("--refetch disabled. Using cached board data...")
        with open(CACHE_FILE_NAME, 'r', encoding="utf8") as f:
            # Load the JSON content
            board_json = json.load(f)
    else:
        logger.info("--refetch enabled. Refetching board data...")
        driver = get_driver(config=config)
        board_json = get_board_json(driver, config)
        with open(CACHE_FILE_NAME, 'w') as f:
            json.dump(board_json, f, indent=4)

    logger.info("Board data retrieved successfully!")
    _, board_members, resolved_board_cards = parse_board(logger,
                                                         config, board_json)

    plot_burndown(logger, board_members,
                  resolved_board_cards, start_date, end_date)


def valid_date(date_string):
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        msg = f"Not a valid date: '{date_string}'."
        raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    main()
