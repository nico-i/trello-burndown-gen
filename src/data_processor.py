import pandas as pd

from src.util.helper import truncate_txt


def create_df(logger, config, board_cards):

    logger.verbose("Plotting burn down chart...")
    # Define the start and end dates for the x-axis.
    start_date = pd.to_datetime(config.start_date, utc=True)
    end_date = pd.to_datetime(config.end_date, utc=True)

    # Filter all cards moved in to the sprint BL list on or the day before the start date
    sprint_cards = []
    for card in board_cards:
        if (card.move_history == None):
            continue
        if(card.current_list.name == config.sprint_bl_list_name):
            sprint_cards.append(card)
            continue
        moved_to_sprint_bl_date = None
        for entry in card.move_history:
            if entry['modified_on'] > start_date and entry['modified_on'] < end_date:
                # was moved to sprint BL during the sprint
                moved_to_sprint_bl_date = entry['modified_on']
        if moved_to_sprint_bl_date != None:
            sprint_cards.append(card)

    total_storypoints = sum(
        [card.story_points for card in sprint_cards])  # Generate the date range

    # Create the 'sprint day' column with the date range
    sprint_days = pd.date_range(start=start_date, end=end_date, freq='D')
    # Calculate the number of days in the sprint
    num_days = (end_date - start_date).days + 1

    actual_storypoints = [total_storypoints] * num_days
    labels = [list()] * num_days

    current_storypoints = total_storypoints

    for day in sprint_days:
        current_labels = list()
        if day == start_date:
            current_labels.append('Sprint start')
        elif day == end_date:
            current_labels.append('Sprint end')

        for card in sprint_cards:
            if card.move_history == None:
                continue
            for entry in card.move_history:
                is_first_move_into_sprint_bl = True
                truncated_card_name = truncate_txt(card.name, 15)
                if entry['modified_on'].date() == day.date():
                    if entry['after_list'].name == config.resolved_list_name:
                        # moved into resolved
                        current_storypoints = current_storypoints - \
                            card.story_points
                        current_labels.append(truncated_card_name)
                    elif entry['after_list'].name == config.sprint_bl_list_name:
                        if is_first_move_into_sprint_bl:
                            is_first_move_into_sprint_bl = False
                            continue
                        # moved back to sprint BL
                        current_storypoints = current_storypoints + \
                            card.story_points
                        current_labels.append(truncated_card_name)
        actual_storypoints[(day - start_date).days] = current_storypoints
        labels[(day - start_date).days] = current_labels
    # Create the DataFrame
    df = pd.DataFrame({
        'sprint day': sprint_days,
        'actual work': actual_storypoints,
        'label': labels
    })
    return df
