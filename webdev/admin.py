from django.contrib import admin

from .models import Comment, Language, Resource, User


class ResourceTimestamp(admin.ModelAdmin):
    readonly_fields = ("timestamp",)


admin.site.register(Comment)
admin.site.register(Language)
admin.site.register(Resource)
admin.site.register(User)
