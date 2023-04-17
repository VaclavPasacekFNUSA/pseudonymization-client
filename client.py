import httpx
import json
import argparse

class CustomAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, token_url: str, refresh_token_url: str, user_data: dict):
        self.token_url = token_url
        self.refresh_token_url = refresh_token_url
        self.access_token = 'token'
        self.refresh_token = 'token'
        self.header = {'Content-Type': 'application/json'}
        self.user_data = user_data

    def auth_flow(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.access_token
        response = yield request
        if response.status_code == 401:
            """ If access token is invalid """
            refresh_token = yield self.get_access_token()
            if response.status_code == 401:
                """ If access token and refresh token are invalid """
                auth_response = yield self.authorize()
                if auth_response.status_code == 401 or auth_response.status_code == 400:
                    raise httpx.RequestError(message=auth_response.text)
                else:
                    tokens = auth_response
                self.access_token, self.refresh_token = tokens.json()['access'], tokens.json()['refresh']
            else:
                self.access_token = refresh_token.json()['access']
            request.headers['Authorization'] = 'Bearer ' + self.access_token
            yield request

    def get_access_token(self):
        data = {"refresh": self.refresh_token}
        return httpx.Request('POST', self.refresh_token_url, data=json.dumps(data), headers=self.header)
    
    def authorize(self):
        return httpx.Request('POST', self.token_url, data=json.dumps(self.user_data), headers=self.header)
    
parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, required=True)
parser.add_argument('--username', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
args, _ = parser.parse_known_args()

data = {"data": args.data}
user_data = {"username": args.username, "password": args.password}
server = 'http://127.0.0.1:8000'

auth = CustomAuth(
    token_url=server + '/v1/token',
    refresh_token_url=server + '/v1/token/refresh',
    user_data=user_data
    )
client = httpx.Client(
    base_url=server,
    headers={'Content-Type': 'application/json'},
    auth=auth,
    )

result = client.put("/v1/randomize", data=json.dumps(data))
print(result.content)



