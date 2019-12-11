from django.contrib import admin

from celeryman import models, tasks


@admin.register(models.Repo)
class RepoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'github_username', 'avatar_url']
    actions = ['fetch_avatar_urls', 'delete_avatar_urls']

    def fetch_avatar_urls(self, request, queryset):
        for obj in queryset:
            tasks.set_github_user_avatar(obj.github_username)
        self.message_user(request, "Fetched avatar URLs")

    def delete_avatar_urls(self, request, queryset):
        queryset.update(avatar_url="")
        self.message_user(request, "Removed avatar URLs")
