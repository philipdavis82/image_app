from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
# Create your views here.

def upload_image_view(request): 
  
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = ImageForm() 
    return render(request, 'image_edit_form.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfully uploaded') 