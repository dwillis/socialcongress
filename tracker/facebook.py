import urllib
import urlparse
import subprocess

def fetch_facebook_token():
    FACEBOOK_APP_ID     = 'APP_ID'
    FACEBOOK_APP_SECRET = 'APP_SECRET'
    # Trying to get an access token. Very awkward.
    oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                      client_secret = FACEBOOK_APP_SECRET,
                      grant_type    = 'client_credentials')
    oauth_response = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)).read()

    try:
        oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
        return oauth_access_token
    except KeyError:
        print('Unable to grab an access token!')
        exit()
