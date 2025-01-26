from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Source ,Income
from django.core.paginator import Paginator
from userpreference.models import UserPreference
from django.contrib import messages
import json
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Income
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import csv

# Allow AJAX requests without CSRF token (only for development; handle CSRF properly in production)

def SearchIncome(request):
    if request.method == "POST":
        try:
            # Parse search text from request body
            search_res = json.loads(request.body).get('searchtext').strip()

            # Fetch income entries for the logged-in user
            income = Income.objects.filter(owner=request.user)
            # Initialize an empty queryset for filtering results
            filtered_income = income.none()

            # Check if the search text is numeric (for amount)
            if search_res.isdigit():
                filtered_income = income.filter(amount__startswith=search_res)

            # Check if the search text is a valid date (YYYY-MM-DD format)
            elif len(search_res) == 10 and search_res[4] == '-' and search_res[7] == '-':
                try:
                    search_date = datetime.strptime(search_res, '%Y-%m-%d').date()
                    filtered_income = income.filter(date=search_date)
                except ValueError:
                    pass  # Ignore invalid date format

            else:
                # Fallback to filtering by description or source (for text search)
                filtered_income = income.filter(
                    description__icontains=search_res
                ) | income.filter(source__icontains=search_res).distinct()

            # Serialize the filtered income into a list of dictionaries
            data = list(filtered_income.values('id', 'amount', 'source', 'description', 'date'))


            # Return the JSON response with the filtered data
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # If not a POST request, return an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def index(request):
    source= Source.objects.all()

    income = Income.objects.filter(owner=request.user)

    paginator = Paginator(income, 4)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency =UserPreference.objects.get(user=request.user).currency


    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,

    }
    return render(request, 'income/index.html',context)


def add_income(request):
    source = Source.objects.all()
    context = {
        'source': source,
        'values': request.POST
    }

    if request.method == "GET":
        return render(request, 'income/add_income.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['expense_date']

        # Validation checks
        if not amount:
            messages.error(request, 'Please enter your amount')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description cannot be empty')
            return render(request, 'income/add_income.html', context)

        if not source:
            messages.error(request, 'Category cannot be empty')
            return render(request, 'income/add_income.html', context)

        if not date:
            messages.error(request, 'Date of expense cannot be empty')
            return render(request, 'income/add_income.html', context)

        # Save the expense to the database (assuming you have an Expense model)
        Income.objects.create(amount=amount, description=description, source=source,date=date,owner=request.user)

        # Redirect to the list of expenses after successful submission
        messages.success(request, 'Income added successfully!')
        return redirect('income')
        # Update 'expenses' to the correct name of your expenses list URL


    # Default fallback (this will never be reached because all methods are handled above)

    return render(request, 'income/add_income.html', context)

def edit_income(request,id):
    income = Income.objects.get(pk=id)
    context = {
        'income': income,
        'values':income,
        'source': Source.objects.all()
    }
    if request.method == "GET":
        return render(request, 'income/edit_income.html', context)

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['expense_date']

        # Validation checks

        if not amount:
            messages.error(request, 'Please enter your amount')
            return render(request, 'income/edit_income.html', context)

        if not description:
            messages.error(request, 'Description cannot be empty')
            return render(request, 'income/edit_income.html', context)

        if not source:
            messages.error(request, 'source cannot be empty')
            return render(request, 'income/edit_income.html', context)

        if not date:
            messages.error(request, 'Date of expense cannot be empty')
            return render(request, 'income/edit_income.html', context)

        # Save the expense to the database (assuming you have an Expense model)
        # Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()


        # Redirect to the list of expenses after successful submission
        messages.success(request, 'Income updated successfully!')
        return redirect('income')

    return render(request, 'income/edit_income.html', context)
def delete_income(request,id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully!')
    return redirect('income')

def income_source_summary(request):
    today_date = datetime.today()
    one_month_ago = today_date - timedelta(days=30)

    # Filter income records for the past month for the logged-in user
    income = Income.objects.filter(
        owner=request.user,
        date__gte=one_month_ago,
        date__lte=today_date
    )

    datafinalrep = {}

    # Function to extract unique sources
    def get_source(income):
        return income.source

    # Get a list of unique sources
    income_sourcelist = list(set(map(get_source, income)))

    # Function to calculate the total amount for a specific source
    def get_source_amount(source):
        amount = 0
        filter_source = income.filter(source=source)

        for item in filter_source:
            amount += item.amount
        return amount

    # Populate the datafinalrep dictionary with source and total amount
    for source in income_sourcelist:
        datafinalrep[source] = get_source_amount(source)

    # Debugging: Print the data to verify correctness
    print("Income Source Summary Data:", datafinalrep)

    return JsonResponse({'source_category_datasets': datafinalrep}, safe=False)



def stats_view_income(request):
    return render(request,'income/stats_income.html')

# Export to CSV
def export_csv(request):
    expenses = Income.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=income.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount', 'source', 'Description', 'Date'])
    for expense in expenses:
        writer.writerow([expense.amount, expense.source, expense.description, expense.date])
    return response

#Export to PDF
def export_pdf(request):
    income = Income.objects.filter(owner=request.user)
    currency = UserPreference.objects.get(user=request.user).currency

    # Calculate the total expense amount
    total_income = sum(expense.amount for expense in income)

    template_path = 'income/pdf_template_income.html'

    # Preparing context for the PDF template
    context = {

        'income': income,
        'currency': currency,
        'total_income': total_income,
        'now': datetime.now(),
    }

    # Render the HTML template to a string
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="income.pdf"'
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse('We had some errors generating your PDF.')

    return response
