from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=254)
    twitter_username = models.CharField(max_length=254, blank=True)
    avatar_url = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name
