import datetime
import platform
from enum import Enum
from typing import List


class Browser(Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"


class Config:
    def __init__(self, browser: str, headless: bool, email: str, password: str, board_url: str, resolved_list_name: str):
        self.resolved_list_name = resolved_list_name
        self.headless = headless
        self.email = email
        self.password = password

        if browser not in [d.value for d in Browser]:
            raise TypeError("driver must be one of the following: %s. Was: '%s'" % ([
                            d.value for d in Browser], browser))
        self.browser = browser

        self.board_url = board_url

    def __repr__(self):
        return "Config(browser='%s', headless=%s, email='%s', password=*****, board_url='%s', resolved_list_name='%s')" % (self.browser, self.headless, self.email, self.board_url, self.resolved_list_name)


class Trello_Card:
    def __init__(self, id: str, name: str, assignee: str, story_points: int, resolved_on: datetime):
        self.id = id
        self.name = name
        self.assignee = assignee
        self.story_points = story_points
        self.resolved_on = resolved_on

    def __repr__(self) -> str:
        return "Trello_Card(id=%s, name=%s, assignee=%s, story_points=%s, resolved_on=%s)" % (self.id, self.name, self.assignee, self.story_points, self.resolved_on)


class Trello_List:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "Trello_List(id=%s, name=%s)" % (self.id, self.name)


class Trello_Member:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "Trello_Member(id=%s, name=%s)" % (self.id, self.name)
