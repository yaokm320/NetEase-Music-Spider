import scrapy
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class MyUseragentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENTS')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent


class MyCookieMiddleware(object):

    def __init__(self, cookies):

        self.cookie = random.choice(cookies)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cookies=crawler.settings.get('COOKIES')
        )

    def process_request(self, request, spider):
        request.cookies = self.cookie
