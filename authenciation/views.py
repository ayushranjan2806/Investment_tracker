from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
import logging
from django.conf import settings
# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'authenciation/regiester.html')
    # Ensure template path matches your directory
    def post(self, request):
        # messages.error(request, 'danger')
        # messages.success(request, 'successfully registered')
        #
        # return render(request,'authenciation/regiester.html')
        #get data
        #validate data
        # create a user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context={
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short.')
                    return render(request, 'authenciation/regiester.html',context)


                # Create the user
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False  # Account is inactive initially
                user.save()

                # Send email to user (after successful registration)
                subject = 'Account Activation'
                message = f'Hello {username},\n\nPlease click the link below to activate your account:\n\n{request.build_absolute_uri("/activate/")}'
                logger = logging.getLogger(__name__)

                try:
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,  # From email
                        [email],  # Recipient email
                        fail_silently=False,
                    )
                    print("Email send attempted.")
                except Exception as e:
                    logger.error(f"Failed to send email: {e}")

                messages.success(request,
                                 'Account created successfully. Please check your email for account activation.')
                  # Redirect to login page

        return render(request, 'authenciation/regiester.html')



class EmailValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)  # Ensure valid JSON is passed
            email = data.get('email', '').strip()  # Get 'email' safely
            if not email:  # Validate that email is provided
                return JsonResponse({'email_error': 'Email field is required'}, status=400)
            if not validate_email(email):  # Check if email format is valid
                return JsonResponse({'email_error': 'Email is invalid'}, status=400)
            if User.objects.filter(email=email).exists():  # Check for duplicate email
                return JsonResponse({'email_error': 'Sorry, email is in use. Choose another one'}, status=409)
            return JsonResponse({'email_valid': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

class validation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)  # Ensure valid JSON is passed
            username = data.get('username', '').strip()  # Get 'username' safely
            if not username:  # Validate that username is provided
                return JsonResponse({'error': 'Username field is required'}, status=400)
            if not str(username).isalnum():  # Check alphanumeric characters
                return JsonResponse({'error': 'Username must contain only alphanumeric characters'}, status=400)
            if User.objects.filter(username=username).exists():  # Check for duplicate username
                return JsonResponse({'error': 'Username already exists'}, status=409)
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
