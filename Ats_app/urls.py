# Ats_app/urls.py
from django.urls import path
from .views import analyze_cv, test_api_connection

app_name = 'ats'  # This allows namespacing

urlpatterns = [
    path('analyze/', analyze_cv, name='analyze_cv'),  # Ensure this line exists
    path('test-api/', test_api_connection, name='test_api'),
]
