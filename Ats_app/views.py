from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
# ats/views.py
#from django.shortcuts import render
from django.conf import settings
from .forms import CVUploadForm
import PyPDF2 as pdf
import google.generativeai as genai
import os
import json

# Configure Google Generative AI
API_KEY = 'AIzaSyDsxuliFs7v-kYT0pEmia7wXgU56iG779o'
genai.configure(api_key=API_KEY)

def get_gemini_response(input_text):
    """Generates a response from the Gemini model using the input text."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text
    return text


def test_api_connection(request):
    try:
        # Test API configuration by making a simple API request
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("test")
        
        # Check if the response is valid
        if response and response.text:
            return JsonResponse({'status': 'success', 'message': 'API connection successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'API connection failed'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def analyze_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv_file = request.FILES['cv']
            job_description = form.cleaned_data['job_description']

            # Extract text from CV
            cv_text = extract_text_from_pdf(cv_file)
            
            # Prepare the prompt for the AI model
            input_prompt = f"""
            Hey Act Like a skilled or very experienced ATS (Applicant Tracking System)
            with a deep understanding of tech fields, software engineering, data science, 
            data analysis, and big data engineering. Your task is to evaluate the resume based 
            on the given job description. The job market is very competitive, and you should 
            provide the best assistance for improving the resumes. Assign a percentage match 
            based on the job description and identify missing keywords with high accuracy.

            Resume: {cv_text}
            Description: {job_description}

            I want the response in one single string having the structure:
            {{ "JD_Match": "%", "MissingKeywords": [], "Profile_Summary": "" }}
            """

            # Get response from the AI model
            response_text = get_gemini_response(input_prompt)
            print("Response Text:", response_text)
            
            # Parse the response
            try:
                response_json = json.loads(response_text)
                return render(request, 'Ats_app/result.html', {'result': response_json})
            except json.JSONDecodeError:
                return render(request, 'Ats_app/result.html', {'error': 'Failed to decode the response from the AI model.'})
    else:
        form = CVUploadForm()

    return render(request, 'Ats_app/upload.html', {'form': form})
