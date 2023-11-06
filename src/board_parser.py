
import json

from src.util.models import TrelloAction, TrelloCard, TrelloList, TrelloMember
import pandas as pd

def parse_lists(board_json):
    return [TrelloList(l['id'], l['name'])
            for l in board_json['lists']]


def parse_members(board_json):
    return [TrelloMember(m['id'], m['fullName'])
            for m in board_json['members']]


def parse_move_actions(board_json):
    return [TrelloAction(a['date'], a['data']['card']['id'], a['data']['listBefore']['id'],
                         a['data']['listAfter']['id']) for a in board_json['actions'] if 'listBefore' in a['data'].keys()]


def parse_board(logger, config, board_json):
    logger.verbose("Parsing board data...")

    board_lists = parse_lists(board_json)
    board_members = parse_members(board_json)
    board_move_actions = parse_move_actions(board_json)

    resolved_list = None
    sprint_bl_list = None

    for l in board_lists:
        if (l.name == config.resolved_list_name):
            resolved_list = l
        elif (l.name == config.sprint_bl_list_name):
            sprint_bl_list = l
        if(sprint_bl_list is not None and resolved_list is not None):
            break

    if (sprint_bl_list is None):
        raise ValueError("Sprint backlog list not found!")

    if (resolved_list is None):
        raise ValueError("Resolved list not found!")

    board_cards = []

    if(config.member_name is not None):
        logger.verbose(
            "Member defined in config, creating burn-down chart only for %s's activity!" % config.member_name)

    for c in board_json['cards']:
        # 'closed' is true for archived cards
        if c['closed'] == True:
            continue

        if len(c['idMembers']) > 1:
            raise ValueError(
                "A card cannot have more than one member! Invalid card: '%s'" % c['name'])
        try:
            assignee = next(
                m for m in board_members if m.id == c['idMembers'][0])
        except Exception:
            if(config.member_name is not None):
                continue
            assignee = None

        if(config.member_name is not None and assignee is not None and config.member_name != assignee.name):
            continue  # skip cards that are not assigned to the member defined in config

        try:
            current_list = next(
                l for l in board_lists if l.id == c['idList'])
        except Exception:
            raise ValueError("List '%s' not found!" % c['idList'])

        c_plugin_data = c['pluginData']
        story_points = None
        story_points_history = None

        if (len(c_plugin_data) <= 0 or c_plugin_data[0]['idPlugin'] != '59d4ef8cfea15a55b0086614'):
            if current_list in [sprint_bl_list, resolved_list]:
                raise ValueError(
                    "Card '%s' has no 'Agile Tools by Corrello' data!" % c['name'])
        else:
            story_points_data = json.loads(c_plugin_data[0]['value'])
            story_points_history = story_points_data['pointsHistory']
            if 'points' not in story_points_data.keys():
                if current_list in [sprint_bl_list, resolved_list]:
                    raise ValueError(
                        "Card '%s' has no story points assigned!" % c['name'])
            else:
                story_points = story_points_data['points']

        card_move_history = []
        for a in board_move_actions:
            if a.card_id == c['id']:
                before_list = next(
                    l for l in board_lists if l.id == a.before_list_id)
                after_list = next(
                    l for l in board_lists if l.id == a.after_list_id)
                card_move_history.append(
                    {'modified_on': pd.to_datetime(a.modified_on), 'before_list': before_list, 'after_list': after_list})

        if(len(card_move_history) == 0):
            card_move_history = None

        board_cards.append(TrelloCard(
            id=c['id'], name=c['name'], assignee=assignee, story_points=story_points, story_points_history=story_points_history, current_list=current_list, move_history=card_move_history))

    logger.info("Board data parsed successfully!")
    if(config.member_name is not None):
        logger.verbose("Number of %s's cards parsed: %s" %
                       (config.member_name, len(board_cards)))
    else:
        logger.verbose("Total cards parsed: %s" % len(board_cards))
    logger.verbose("Board members: %s" % len(board_members))
    logger.verbose("Board lists: %s" % len(board_lists))
    return board_lists, board_members, board_cards
