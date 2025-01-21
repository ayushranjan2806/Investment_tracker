from django.views.decorators.csrf import csrf_exempt

from .views import RegisterView, validation,  EmailValidationView
from django.urls import path
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('validate-username',csrf_exempt(validation.as_view()), name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()), name='validate-email'),

]
