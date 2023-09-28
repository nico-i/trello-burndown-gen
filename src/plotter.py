
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil import tz
from matplotlib.dates import date2num

from util.constants import DATE_FORMAT
from util.helper import truncate_txt


def plot_burndown(logger, board_members, resolved_board_cards, start_date, end_date):
    logger.verbose("Plotting burndown chart...")
    # Define the start and end dates for the x-axis.
    # Define a specific start_date
    start_date = pd.to_datetime(start_date, utc=True)
    # Define a specific end_date
    end_date = pd.to_datetime(end_date, utc=True)

    # Generate a list of all dates between start_date and end_date
    all_dates = [start_date + timedelta(days=i)
                 for i in range((end_date - start_date).days + 1)]

    data = {}
    max_story_points = 0
    for member in board_members:
        cum_sum = 0.1
        member_data = {
            "dates": [start_date],
            "story_points": [cum_sum],
            "labels": [""]
        }
        for card in resolved_board_cards:
            if card.assignee.name == member.name:
                member_data["dates"].append(pd.to_datetime(card.resolved_on, utc=True)
                                            )
                cum_sum += card.story_points
                member_data["story_points"].append(cum_sum)
                member_data["labels"].append(truncate_txt(card.name, 18))

        if cum_sum > max_story_points:
            max_story_points = cum_sum

        member_data["dates"].append(end_date)
        member_data["story_points"].append(max_story_points)
        member_data["labels"].append("")

        data[member.name] = pd.DataFrame(member_data)

    # Loop through the dictionary and plot each DataFrame
    for name, df in data.items():
        if not df.empty:
            # Convert 'dates' column to datetime
            df['dates'] = pd.to_datetime(df['dates'])

            # Sort dataframe by 'dates'
            df = df.sort_values('dates')

            # Plotting
            plt.plot(df['dates'], df['story_points'])
            plt.fill_between(df['dates'], df['story_points'],
                             label=name, alpha=0.5)

    for i, row in df.iterrows():
        plt.annotate(row['labels'], (row['dates'], row['story_points']),
                     textcoords="offset points", xytext=(0, 8), ha='center', fontsize=7)

    # x-axis
    plt.xlabel('Dates')
    plt.xlim(start_date, end_date)
    plt.xticks(all_dates, labels=[date.strftime(DATE_FORMAT)
                                  for date in all_dates], rotation=45, ha='right')
    # y-axis
    plt.ylabel('Cumulative Story Points')
    plt.yticks(range(0,   np.ceil((max_story_points +
                                   max_story_points/2)).astype(int), 1))
    # plot settings
    plt.tight_layout()
    plt.title('Burndown Chart from %s to %s' % (start_date.strftime(
        DATE_FORMAT), end_date.strftime(DATE_FORMAT)))
    plt.legend(loc='upper left')

    logger.info("Burndown chart plotted successfully!")
    logger.verbose("Showing burndown chart...")

    plt.show()
