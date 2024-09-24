from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CVForm
from .models import CV

# Home page view
def home(request):
    return render(request, 'CV_app/home.html')

# Login view
class CustomLoginView(View):
    def get(self, request):
        return render(request, 'CV_app/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'CV_app/login.html')

# Logout view
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')  # Redirect to home page after logout

# Signup view
class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'CV_app/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to login after signup
        return render(request, 'CV_app/signup.html', {'form': form})

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'CV_app/dashboard.html')

# Create CV view
@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user  # Associate the CV with the logged-in user
            cv.save()
            messages.success(request, 'CV created successfully!')
            return redirect('dashboard')  # Redirect to dashboard after creating CV
    else:
        form = CVForm()
    return render(request, 'CV_app/create_cv.html', {'form': form})
