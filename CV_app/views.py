#CV_app/View.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import CVForm
from .models import CV
from django.http import HttpResponse


# Home page view
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if logged in
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
        form = CustomUserCreationForm()
        return render(request, 'CV_app/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to login after signup
        else:
            messages.error(request, 'Please correct the errors below.')
        
        # Return the form with the errors and filled data
        return render(request, 'CV_app/signup.html', {'form': form})


# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'CV_app/dashboard.html')


@login_required
def download_cv(request, cv_id):
    cv = CV.objects.get(id=cv_id)
    html_content = render_to_string('CV_app/cv_template.html', {'cv': cv})
    pdf = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.name}_cv.pdf"'
    return response

# Create CV view
@login_required
def create_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            messages.success(request, 'CV created successfully!')

            # Generate PDF
            return redirect('dashboard')  # Redirect to dashboard after creating CV
    else:
        form = CVForm()
    return render(request, 'CV_app/create_cv.html', {'form': form})
