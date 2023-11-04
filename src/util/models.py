import datetime
import platform
from enum import Enum
from typing import List


class Browser(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"


class Config:
    def __init__(self, browser: str, headless: bool, email: str, password: str, board_url: str, sprint_bl_list_name: str, resolved_list_name: str, member_name: str = None):
        self.resolved_list_name = resolved_list_name
        self.sprint_bl_list_name = sprint_bl_list_name
        self.headless = headless
        self.email = email
        self.password = password
        self.member_name = member_name

        if browser not in [d.value for d in Browser]:
            raise TypeError("driver must be one of the following: %s. Was: '%s'" % ([
                            d.value for d in Browser], browser))
        self.browser = browser
        self.board_url = board_url

    def __repr__(self):
        return "Config(browser='%s', headless= % s, email='%s', password=*****, board_url='%s',  sprint_bl_list_name='%s' resolved_list_name='%s')" % (self.browser, self.headless, self.email, self.board_url, self.sprint_bl_list_name, self.resolved_list_name)


class TrelloCard:
    def __init__(self, id: str, name: str, assignee: any, story_points: int, story_points_history: list, current_list: any, move_history: list):
        self.id = id
        self.name = name
        self.assignee = assignee  # TrelloMember
        self.story_points = story_points
        self.story_points_history = story_points_history
        self.current_list = current_list
        self.move_history = move_history

    def __repr__(self):
        return "Trello_Card(id=%s, name=%s, assignee=%s, story_points_history=%s, move_history=%s)" % (self.id, self.name, self.assignee_name, self.story_points_history, self.move_history)


class TrelloAction:
    def __init__(self, modified_on: datetime, card_id: str, before_list_id: str, after_list_id: str):
        self.modified_on = modified_on
        self.card_id = card_id
        self.before_list_id = before_list_id
        self.after_list_id = after_list_id

    def __repr__(self) -> str:
        return "Trello_Action(modified_on=%s, card_id=%s, before_list_id=%s, after_list_id=%s)" % (self.modified_on, self.card_id, self.before_list_id, self.after_list_id)


class TrelloList:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "Trello_List(id=%s, name=%s)" % (self.id, self.name)


class TrelloMember:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "Trello_Member(id=%s, name=%s)" % (self.id, self.name)
