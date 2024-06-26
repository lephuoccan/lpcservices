import requests

class LPCProxyAPI(object):

    API_STATUS_PATH = "/api/v1/status"
    API_RESET_PATH = "/api/v1/reset"
    API_PROFILE_LIST_PATH = "/api/v3/profiles"
    API_DELETE_PATH = "/api/v3/delete"

    _apiUrl = ''
    def __init__(self, apiUrl: str):
        self._apiUrl = apiUrl
    
    def GetStatus(self):
        try:
            url = f"{self._apiUrl}{self.API_STATUS_PATH}?proxy=all"
            print(url)
            resp = requests.get(url)
            return resp.json()
        except:
            print('error GetStatus()')
            return None