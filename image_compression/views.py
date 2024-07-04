from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CompressImageForm
from PIL import Image
import io

# Create your views here.

def compress(request):
    user = request.user # user who's logged in
    
    if request.method == "POST":
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_image = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']
            
            compressed_image = form.save(commit=False) # temporarily saving form
            compressed_image.user = user
            
            # Perform compression
            img = Image.open(original_image)
            output_format = img.format # get images format
            
            buffer = io.BytesIO() # buffer to store image's binary data.
            # print('blank buffer =>', buffer.getvalue())
            
            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0) # Move buffer's internal cursor to the beginning of the written data, so wen can later read it or write.
            
            # print(f"Cursor position at after setting back to 0 => ", buffer.tell())
            # print('buffer =>', buffer.getvalue())
            
            # compressed image inside the Model
            compressed_image.compressed_img.save(
                f'compressed_{original_image}', buffer
            )
            
            # Download compressed file.
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_image}'
            return response
            # return redirect('compress')
            
    else:
        image_form = CompressImageForm()
        context = {
            'image_form':image_form
        }
        return render(request, 'image_compression/compress.html', context)