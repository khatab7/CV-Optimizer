from django import forms

class CVUploadForm(forms.Form):
    cv = forms.FileField(label='Upload CV (PDF format)')
    job_description = forms.CharField(widget=forms.Textarea, label='Enter Job Description')
