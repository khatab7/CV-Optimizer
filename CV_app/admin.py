from django.contrib import admin
from .models import CV

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')  # Add other fields as needed
    search_fields = ('name', 'email')  # Add searchable fields
