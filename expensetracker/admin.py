from django.contrib import admin
from .models import Expense, Category

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'description', 'owner', 'category')  # Fields to display in the list view
    search_fields = ('owner__username', 'category', 'description')  # Enable searching by owner, category, and description
    list_filter = ('date', 'category')  # Add filters for date and category
    ordering = ('-date',)  # Order the list by date in descending order

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name field in the list view
    search_fields = ('name',)  # Enable searching by category name
    ordering = ('-name',)  # Order the list by name in descending order

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
