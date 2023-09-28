
import json

from dateutil import parser

from util.models import Trello_Card, Trello_List, Trello_Member


def parse_board(logger, config, board_json):
    logger.verbose("Parsing board data...")

    board_lists = [Trello_List(l['id'], l['name'])
                   for l in board_json['lists']]

    board_members = [Trello_Member(m['id'], m['fullName'])
                     for m in board_json['members']]

    resolved_list_id = None

    for l in board_lists:
        if (l.name == config.resolved_list_name):
            resolved_list_id = l.id
            break

    if (resolved_list_id is None):
        raise ValueError("Sprint backlog list not found!")

    resolved_board_cards = []

    for c in board_json['cards']:
        if c['idList'] == resolved_list_id and c['closed'] == False:
            c_members = c['idMembers']
            if len(c_members) <= 0:
                raise ValueError("Card '%s' has no members!" % c['name'])

            story_assignee = None
            for m in board_members:
                if m.id == c_members[0]:
                    story_assignee = m
                    break

            if story_assignee is None:
                raise ValueError("Card '%s' has no assignee!" % c['name'])

            c_plugin_data = c['pluginData']
            if len(c_plugin_data) <= 0:
                raise ValueError(
                    "Card '%s' has no 'Agile Tools by Corrello' data!" % c['name'])

            story_points_data = json.loads(c_plugin_data[0]['value'])

            if 'points' not in story_points_data:
                raise ValueError("Card '%s' has no story points!" % c['name'])
            resolved_date = parser.parse(c['dateLastActivity']).date()
            resolved_board_cards.append(Trello_Card(
                id=c['id'], name=c['name'], assignee=story_assignee, story_points=story_points_data['points'], resolved_on=resolved_date))

    logger.info("Board data parsed successfully!")
    logger.verbose("Resolved cards: %s" % len(resolved_board_cards))
    logger.verbose("Board members: %s" % len(board_members))
    logger.verbose("Board lists: %s" % len(board_lists))
    return board_lists, board_members, resolved_board_cards
