from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=254)
    github_username = models.CharField(max_length=254, blank=True)
    avatar_url = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name


class Repo(models.Model):
    title = models.CharField(max_length=254)
    html_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(to=Author, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
