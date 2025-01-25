from django.shortcuts import render, redirect
from django.contrib import messages

from userpreference.models import UserPreference
from . import models
from .models import Expense
from expensetracker.models import Category
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from io import BytesIO
from .models import Expense
import csv
from django.shortcuts import render
from django.template.loader import render_to_string
from io import BytesIO
from .models import Expense
import json
from datetime import datetime, timedelta
from django.db.models import Sum
from xhtml2pdf import pisa
from django.template.loader import get_template

def SearchExpenses(request):
    if request.method == "POST":
        search_res = json.loads(request.body).get('searchtext').strip()

        expenses = Expense.objects.filter(owner=request.user)

        # Check if the search text is numeric (for amount)
        if search_res.isdigit():
            expenses = expenses.filter(amount__startswith=search_res)

        # Check if the search text is a valid date (YYYY-MM-DD format)
        elif len(search_res) == 10 and search_res[4] == '-' and search_res[7] == '-':
            try:
                # Try parsing the date directly
                search_date = datetime.strptime(search_res, '%Y-%m-%d').date()
                expenses = expenses.filter(date=search_date)
            except ValueError:
                # If it's not a valid date, we just keep the expenses as is
                pass
        else:
            # Fallback to filtering by description or category (for text search)
            expenses = expenses.filter(
                description__icontains=search_res
            ) | expenses.filter(category__icontains=search_res)

        # Serialize the filtered expenses into a list
        data = list(expenses.values())

        # Return the JSON response with the filtered data
        return JsonResponse(data, safe=False)

    # If not a POST request, return an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def index(request):
    categories = Category.objects.all()

    expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 4)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency =UserPreference.objects.get(user=request.user).currency


    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,

    }
    return render(request, 'expenses/index.html',context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == "GET":
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        # Validation checks
        if not amount:
            messages.error(request, 'Please enter your amount')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'Description cannot be empty')
            return render(request, 'expenses/add_expenses.html', context)

        if not category:
            messages.error(request, 'Category cannot be empty')
            return render(request, 'expenses/add_expenses.html', context)

        if not date:
            messages.error(request, 'Date of expense cannot be empty')
            return render(request, 'expenses/add_expenses.html', context)

        # Save the expense to the database (assuming you have an Expense model)
        Expense.objects.create(amount=amount, description=description, category=category,date=date,owner=request.user)

        # Redirect to the list of expenses after successful submission
        messages.success(request, 'Expense added successfully!')
        return redirect('expenses')
        # Update 'expenses' to the correct name of your expenses list URL


    # Default fallback (this will never be reached because all methods are handled above)

    return render(request, 'expenses/add_expenses.html', context)
def edit_expenses(request,id):
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values':expense,
        'categories': Category.objects.all()
    }
    if request.method == "GET":
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense_date']

        # Validation checks
        if not amount:
            messages.error(request, 'Please enter your amount')
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.error(request, 'Description cannot be empty')
            return render(request, 'expenses/edit_expense.html', context)

        if not category:
            messages.error(request, 'Category cannot be empty')
            return render(request, 'expenses/edit_expense.html', context)

        if not date:
            messages.error(request, 'Date of expense cannot be empty')
            return render(request, 'expenses/edit_expense.html', context)

        # Save the expense to the database (assuming you have an Expense model)
        # Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()


        # Redirect to the list of expenses after successful submission
        messages.success(request, 'Expense updated successfully!')
        return redirect('expenses')

    return render(request, 'expenses/edit_expense.html', context)
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('expenses')

def expense_category_summary(request):
    today_date=datetime.today()
    one_month_ago=today_date-timedelta(days=30)
    expenses = Expense.objects.filter(owner=request.user,
        date__gte=one_month_ago,date__lte=today_date)
    datafinalrep={}
    def get_category(expense):
        return expense.category

    categorylist=list(set(map(get_category, expenses)))

    def get_category_amount(category):
        amount=0
        filter_category=expenses.filter(category=category)

        for item in filter_category:
            amount += item.amount
        return amount



    for y in categorylist:
        datafinalrep[y]=get_category_amount(y)
    return JsonResponse({'expense_category_datasets': datafinalrep }, safe=False)




def stats_view(request):
    return render(request,'expenses/stats.html')


# Export to CSV
def export_csv(request):
    expenses = Expense.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Description', 'Date'])
    for expense in expenses:
        writer.writerow([expense.amount, expense.category, expense.description, expense.date])
    return response

# Export to PDF
def export_pdf(request):
    expenses = Expense.objects.filter(owner=request.user)
    currency = UserPreference.objects.get(user=request.user).currency

    # Calculate the total expense amount
    total_expense = sum(expense.amount for expense in expenses)

    template_path = 'expenses/pdf_template.html'

    # Preparing context for the PDF template
    context = {

        'expenses': expenses,
        'currency': currency,
        'total_expense': total_expense,
        'now': datetime.now(),
    }

    # Render the HTML template to a string
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse('We had some errors generating your PDF.')

    return response




