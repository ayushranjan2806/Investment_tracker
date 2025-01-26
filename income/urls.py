from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("", views.index, name="income"),

    path("add_income/", views.add_income, name="add_income"),

    path("edit_income/<int:id>", views.edit_income, name="edit_income"),
    path("income_delete/<int:id>", views.delete_income, name="income_delete"),

    path('search-income',csrf_exempt(views.SearchIncome), name='search_income'),

    path('income_source_summary', views.income_source_summary, name='income_source_summary'),

    path('stats_income', views.stats_view_income, name='stats_income'),

    path('export_csv', views.export_csv, name='export_csv'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
]
