
from django.contrib import admin
from .models import UserPreference

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency')  # Display these fields in the admin list view
    search_fields = ('user__username', 'currency')  # Enable searching by user username and currency
    list_filter = ('currency',)  # Filter by currency
    ordering = ('user',)  # Order the list by user

admin.site.register(UserPreference, UserPreferenceAdmin)
