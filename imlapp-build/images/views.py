from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.urls import reverse
import os
from .forms import *
from imlapp import settings
from PIL import Image
# Create your views here.

# END


# default_storage.DEFAULT_FILE_STORAGE = 'storages.backends.overwrite.OverwriteStorage'

class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template)


from django.shortcuts import redirect

IMAGES_DIR = os.path.join("images","static","images")

class ImageSelect(LoginRequiredMixin, View):
    template = 'image_select.html'
    login_url = '/login/'

    def get(self, request):
        
        pagedata = {
            "image_found" : 0
        }
        try:
            directory = os.path.join(settings.BASE_DIR,IMAGES_DIR,request.user.username)
            file_name = os.path.join(directory,"original."+"jpg")
            file = default_storage.open(file_name)
            pagedata["image_found"] = 1
            im = Image.open(file_name)
            im.thumbnail((256,256))
            thmb = os.path.join(directory,"display."+"jpg")
            im.save(thmb,"JPEG")
            pagedata["img"] = thmb 
        except Exception as e:
            print(e)
            pass
        # Here, Load the current file if there is one. If not load the image upload graphic
        # file = default_storage.open(file_name_op)
        # file_url = default_storage.url(file_name_op)
        # print(self.template)
        return render(request, self.template, pagedata)


def upload_image(request):
    """
    Save two versions of the image as jpgs.
    - One version will be the original that will be operated on each time the view is updated.
    - The second is the current result of the operation.

    TODO:
        - Convert the image to jpg
    """
    #  Saving POST'ed file to storage
    file = request.FILES['img']
    directory = os.path.join(settings.BASE_DIR,IMAGES_DIR,request.user.username)
    try:
        os.mkdir(directory)
    except:
        print("Directory Exists")
    og_file_name = os.path.join(directory,"original."+file.name.split(".")[-1])
    cr_file_name = os.path.join(directory,"current."+file.name.split(".")[-1])
    try:
        os.remove(og_file_name)
    except:
        pass
    try: 
        os.remove(cr_file_name)
    except: 
        pass
    print(file.name)
    file_name = default_storage.save(og_file_name, file)
    file_name_op = default_storage.save(cr_file_name, file)
    print(file_name)
    #  Reading file from storage
    # file = default_storage.open(file_name)
    # file_url = default_storage.url(file_name)
    # file = default_storage.open(file_name_op)
    # file_url = default_storage.url(file_name_op)
    return redirect("/images/image_select/")
    
class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        request.user = authenticate(request, username=username, password=password)        
        if request.user is not None:
            login(request, request.user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})


def upload_image_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'image_edit_form.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')
