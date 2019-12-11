import requests

from celeryman import models


GITHUB_API_BASE = "https://api.github.com/users/"


def set_github_user_avatar(username):
    response = requests.get(f"{GITHUB_API_BASE}{username}")
    json = response.json()
    avatar_url = json["avatar_url"]
    author = models.Author.objects.get(github_username=username)
    author.avatar_url = avatar_url
    author.save()
