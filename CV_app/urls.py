from django.urls import path
from .views import home, CustomLoginView, LogoutView, SignUpView, dashboard, create_cv

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    path('signup/', SignUpView.as_view(), name='signup'),  # Signup page
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard page
    path('create_cv/', create_cv, name='create_cv'),  # Create CV page
]
