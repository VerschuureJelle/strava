import requests

response = requests.post(
    'https://www.strava.com/oauth/token',
    data={
        'client_id': '165778',
        'client_secret': '9446efceef121cc98597b8014609a8d8cdb9786b',
        'code': '3cc263a0eea567a877acb1cf653e1951a8ab7e7b',
        'grant_type': 'authorization_code'
    }
)

print(response.json())
