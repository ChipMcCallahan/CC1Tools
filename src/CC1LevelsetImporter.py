import requests
from html.parser import HTMLParser

CCX_FILES = {"CCLP1", "CCLXP2", "CCLP3", "CCLP4"}
CCX_PREFIX = "https://storage.googleapis.com/file-hosting-abcdef/chips/"
GLIDERBOT_PREFIX = "https://bitbusters.club/gliderbot/sets/cc1/"


class HTMLParserForDAT(HTMLParser):
    def __init__(self):
        self.results = []
        super(HTMLParserForDAT, self).__init__()

    def handle_data(self, data):
        if data.endswith(".dat"):
            self.results.append(data)


class CC1LevelsetImporter:
    def __init__(self):
        self.available_sets = None
        self.cache = dict()

    def get_available_sets_list(self):
        if not self.available_sets:
            parser = HTMLParserForDAT()
            parser.feed(requests.get(GLIDERBOT_PREFIX).text)
            self.available_sets = parser.results
        return self.available_sets
    
    def get_set(self, levelset):
        return_set = None
        if levelset in self.cache:
            return_set = self.cache[levelset]
        if not self.available_sets:
            self.get_available_sets_list()
        if levelset not in self.available_sets:
            raise Exception(f"CC1Levelset {levelset} was not found. Try get_available_sets_list for all options.")
        resp = requests.get(GLIDERBOT_PREFIX + levelset)

        if resp.status_code < 300:
            print(f"Successfully retrieved {GLIDERBOT_PREFIX + levelset}.")
            self.cache[levelset] = resp.content
            return_set = resp.content
        else:
            raise Exception(f"Failed to retrieve {GLIDERBOT_PREFIX + levelset}. {resp.status_code}: {resp.reason}")
        
        return_ccx = None
        if return_set and levelset[:-4] in CCX_FILES:
            resp = requests.get(f"{CCX_PREFIX}{levelset[:-4]}.ccx")
            if resp.status_code < 300:
                print(f"Successfully retrieved {CCX_PREFIX}{levelset[:-4]}.ccx")
                return_ccx = resp.text
            else:
                raise Exception(f"Failed to retrieve {CCX_PREFIX}{levelset[:-4]}.ccx. {resp.status_code}: {resp.reason}")
        
        return return_set, return_ccx