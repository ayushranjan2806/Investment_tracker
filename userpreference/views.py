from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages


def index(request):
    # Load currency data from the JSON file
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})
    except FileNotFoundError:
        messages.error(request, "Currency data file not found.")
        return render(request, 'preference/index.html', {'currencies': [], 'user_preferences': None})

    # Retrieve user preferences (from DB for logged-in users, or session for guests)
    user_preferences = None
    if request.user.is_authenticated:
        user_preferences = UserPreference.objects.filter(user=request.user).first()
    else:
        user_preferences = request.session.get('user_currency', None)

    if request.method == 'GET':
        return render(request, 'preference/index.html', {
            'currencies': currency_data,
            'user_preferences': user_preferences
        })
    elif request.method == 'POST':
        currency = request.POST.get('currency', None)
        if not currency:
            messages.error(request, "Please select a valid currency.")
            return render(request, 'preference/index.html', {
                'currencies': currency_data,
                'user_preferences': user_preferences
            })

        if request.user.is_authenticated:
            # Save preference to the database for logged-in users
            if user_preferences:
                user_preferences.currency = currency
                user_preferences.save()
            else:
                UserPreference.objects.create(user=request.user, currency=currency)
        else:
            # Save preference in the session for guests
            request.session['user_currency'] = currency

        messages.success(request, "Currency preference saved successfully.")
        return redirect('preference')
