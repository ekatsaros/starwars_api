from django.contrib import admin

# Register your models here.
from .models import ApiUser


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "first_name", "last_name")
    readonly_fields = ("id", "date_joined", "last_login")
    search_fields = ("email", "username", "first_name", "last_name")


admin.site.register(ApiUser, UserAdmin)
