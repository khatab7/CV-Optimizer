# ats/urls.py
from django.urls import path
from .views import analyze_cv, test_api_connection

urlpatterns = [
    path('', analyze_cv, name='analyze_cv'),
    path('analyze/', analyze_cv, name='analyze_cv'),
    path('test-api/', test_api_connection, name='test_api_connection'),
]
