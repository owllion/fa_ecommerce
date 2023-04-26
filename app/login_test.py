
from decouple import config
from requests_oauthlib import OAuth2Session

client_id = config("GITHUB_CLIENT_ID")
client_secret = config("GITHUB_CLIENT_SECRET")

github = OAuth2Session(client_id)

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
github.fetch_token(
    token_url, 
    client_secret=client_secret,
    authorization_response=redirect_response
)

# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user')
print(r.content,'this is r.content')