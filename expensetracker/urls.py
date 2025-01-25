from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("", views.index, name="expenses"),

    path("add_expense/", views.add_expense, name="add_expense"),

    path("edit_expense/<int:id>", views.edit_expenses, name="edit_expense"),
    path("expense_delete/<int:id>", views.delete_expense, name="expense_delete"),

    path('search-expenses',csrf_exempt(views.SearchExpenses), name='search_expenses'),

    path('expense_category_summary', views.expense_category_summary, name='expense_category_summary'),

    path('stats',views.stats_view, name='stats'),

    path('export_csv', views.export_csv, name='export_csv'),

    path('export-pdf/', views.export_pdf, name='export_pdf'),







]
