# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from authlib.integrations.starlette_client import OAuth

from .env import TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET

OAUTH = OAuth()
OAUTH.register(
    name="twitter",
    client_id=TWITTER_CLIENT_ID,
    client_secret=TWITTER_CLIENT_SECRET,
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authenticate"
)
