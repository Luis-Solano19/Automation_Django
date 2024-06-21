from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

# Create your views here.

def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        
        # store this file inside the Upload model
        upload = Upload.objects.create(file=file_path, model_name = model_name)
        
        # construct the full path for file
        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        
        # making absolute path
        absolute_file_path = str(upload.file.path)
        
        # trigger the import data command
        try:
            call_command('importdata', absolute_file_path, model_name) # importdata was command created before
            messages.success(request, 'Data from CSV imported successfully! ')
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('import_data')
    
    else:
        custom_models = get_all_custom_models()
        context = {
            'all_models':custom_models
        }
    return render(request, 'dataentry/importdata.html', context)
