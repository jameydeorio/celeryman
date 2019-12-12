from django.contrib import admin

from celeryman import models, tasks


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'twitter_username', 'avatar_url']
    actions = ['fetch_avatar_urls', 'delete_avatar_urls']

    def fetch_avatar_urls(self, request, queryset):
        for obj in queryset:
            tasks.set_twitter_user_avatar.delay(obj.twitter_username)
        self.message_user(request, "Fetching avatar URLs...")

    def delete_avatar_urls(self, request, queryset):
        queryset.update(avatar_url="")
        self.message_user(request, "Removed avatar URLs")
