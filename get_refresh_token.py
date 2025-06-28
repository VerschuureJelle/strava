import requests

CLIENT_ID = '165778'
CLIENT_SECRET = '9446efceef121cc98597b8014609a8d8cdb9786b'
AUTHORIZATION_CODE = '3573abe3acead0ab32f8b11c5cbc3ac436da46e3'

response = requests.post(
    'https://www.strava.com/oauth/token',
    data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTHORIZATION_CODE,
        'grant_type': 'authorization_code'
    }
)

print(response.json())
