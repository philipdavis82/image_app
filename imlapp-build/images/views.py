from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
import os
from .forms import *
# Create your views here.


class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        return render(request, self.template)


from django.shortcuts import redirect

class ImageSelect(LoginRequiredMixin, View):
    template = 'image_select.html'
    login_url = '/login/'

    def get(self, request):
        pagedata = {}
        # Here, Load the current file if there is one. If not load the image upload graphic
        # file = default_storage.open(file_name_op)
        # file_url = default_storage.url(file_name_op)
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
    os.mkdir(request.user.username)
    file_name = default_storage.save(request.user.username+"/"+"original."+file.name.split(".")[-1], file)
    file_name_op = default_storage.save(request.user.username+"/"+"current."+file.name.split(".")[-1], file)
    #  Reading file from storage
    # file = default_storage.open(file_name)
    # file_url = default_storage.url(file_name)
    # file = default_storage.open(file_name_op)
    # file_url = default_storage.url(file_name_op)
    return redirect(request,"images/image_select/")

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
