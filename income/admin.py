from django.contrib import admin
from .models import Income, Source

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'description', 'owner', 'source')  # Fields to display in the list view
    search_fields = ('owner__username', 'source', 'description')  # Enable searching by owner, source, and description
    list_filter = ('date', 'source')  # Add filters for date and source
    ordering = ('-date',)  # Order the list by date in descending order

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name field in the list view
    search_fields = ('name',)  # Enable searching by source name
    ordering = ('-name',)  # Order the list by name in descending order

admin.site.register(Income, IncomeAdmin)
admin.site.register(Source, SourceAdmin)
