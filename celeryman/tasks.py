import base64

import requests

from chassis.core.celery import app
from django.conf import settings
from django.core.cache import cache

from celeryman import models


def get_twitter_token():
    token = cache.get('twitter_token')
    if not token:
        user_pass = f"{settings.TWITTER_CONSUMER_KEY}:{settings.TWITTER_CONSUMER_SECRET}"
        basic_auth = base64.b64encode(user_pass.encode("utf-8"))
        headers = {
            "Authorization": f"Basic {basic_auth.decode('utf-8')}"
        }
        response = requests.post("https://api.twitter.com/oauth2/token",
                                 data={"grant_type": "client_credentials"},
                                 headers=headers)
        json = response.json()
        token = json["access_token"]
        cache.set("twitter_token", token)
    return token


@app.task
def set_twitter_user_avatar(username):
    headers = {
        "Authorization": f"Bearer {get_twitter_token()}"
    }
    response = requests.get("https://api.twitter.com/1.1/users/show.json",
                            params={"screen_name": username},
                            headers=headers)
    json = response.json()
    if "profile_image_url" not in json:
        return
    avatar_url = json["profile_image_url"]
    author = models.Author.objects.get(twitter_username=username)
    author.avatar_url = avatar_url
    author.save()


@app.task
def fetch_avatar_urls():
    for author in models.Author.objects.all():
        set_twitter_user_avatar(author.twitter_username)
