from django.shortcuts import render, redirect
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
# from django.core.management import call_command
from django.contrib import messages
from .tasks import import_data_task, export_data_task
from django.core.management import call_command
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
        
        #check for CSV errors
        try:
            check_csv_errors(absolute_file_path, model_name) # if this fails will return error
        
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')
        
        
        # handle the import data task here
        import_data_task.delay(absolute_file_path, model_name)
        
        # code commented below was taken to tasks.py on dataentry
        # trigger the import data command
        # try:
        #     call_command('importdata', absolute_file_path, model_name) # importdata command created before
        #     messages.success(request, 'Data from CSV imported successfully! ')
        # except Exception as e:
        #     messages.error(request, str(e))
        
        # show message to user
        messages.success(request, 'Your data is being imported, you will be notified once it finishes.')
        return redirect('import_data')
    
    else:
        custom_models = get_all_custom_models()
        context = {
            'all_models':custom_models
        }
    return render(request, 'dataentry/importdata.html', context)


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get('model_name')
        
        # call the export data task
        export_data_task.delay(model_name)
        
        # show message to user
        messages.success(request, 'Your data is being exported, you will be notified once it finishes.')
        return redirect('export_data')
    else:
        models = get_all_custom_models()
        context = {
            'all_models':models
        }  
    return render(request, 'dataentry/exportdata.html', context)
