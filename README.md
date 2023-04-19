# pseudonymization-client

### Code for importing client and getting response
```
from client import CustomAuth, httpx, json


data = {"data": "some_data"}
user_data = {"username": "acc_username", "password": "acc_password"}
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
```
