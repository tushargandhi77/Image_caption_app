# captioner/views.py
from django.shortcuts import render
from .forms import CaptionForm
from .utils import generate_captions
from django.conf import settings
import os
from .models import Caption

def cleanup_old_files(request):
    # Clean up old image if it exists in session
    if 'last_image_id' in request.session:
        try:
            old_caption = Caption.objects.get(id=request.session['last_image_id'])
            # Delete the image file
            if old_caption.image:
                if os.path.exists(old_caption.image.path):
                    os.remove(old_caption.image.path)
            # Delete the Caption object
            old_caption.delete()
        except Caption.DoesNotExist:
            pass
    
def home(request):
    # Clear previous data on page load (GET request)
    if request.method == 'GET':
        cleanup_old_files(request)
        # Clear session data
        request.session['last_image_id'] = None
        return render(request, 'captioner/home.html', {'form': CaptionForm()})

    captions = None
    if request.method == 'POST':
        # Clean up old files first
        cleanup_old_files(request)
        
        form = CaptionForm(request.POST, request.FILES)
        if form.is_valid():
            caption_obj = form.save()
            
            # Store new image id in session
            request.session['last_image_id'] = caption_obj.id
            
            # Generate captions
            try:
                image_path = os.path.join(settings.MEDIA_ROOT, str(caption_obj.image))
                generated_text = generate_captions(
                    image_path,
                    caption_obj.platform,
                    caption_obj.num_captions
                )
                # Split the captions into a list
                captions = [cap.strip() for cap in generated_text.split('\n') if cap.strip()]
                caption_obj.generated_captions = generated_text
                caption_obj.save()
            except Exception as e:
                # If there's an error, cleanup the uploaded file
                if caption_obj.image:
                    if os.path.exists(caption_obj.image.path):
                        os.remove(caption_obj.image.path)
                caption_obj.delete()
                form = CaptionForm()
                return render(request, 'captioner/home.html', {
                    'form': form, 
                    'error': 'Error processing image. Please try again.'
                })
    else:
        form = CaptionForm()
    
    return render(request, 'captioner/home.html', {'form': form, 'captions': captions})