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
        return render(request, self.template)


def upload_image(request):
    #  Saving POST'ed file to storage
    file = request.FILES['img']
    os.mkdir(request.user.username)
    file_name = default_storage.save(request.user.username+"/"+file.name, file)
    #  Reading file from storage
    file = default_storage.open(file_name)
    file_url = default_storage.url(file_name)


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
