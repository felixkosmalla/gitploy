from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as ulogin, logout as ulogout
from django.contrib import messages

from deployments.models import *


@login_required
def index(request):

    return render(request, "index.html", {'projects':Project.objects.all()})


def login(request):


    if (request.method == "POST"):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:


            if user.is_active:
                messages.add_message(request, messages.SUCCESS, 'Login Successful')
                ulogin(request, user)
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                try:
                    if request.GET['next']:
                        return redirect(request.GET['next'])
                except:
                    pass

            else:
                messages.add_message(request, messages.ERROR, 'User inactive')
        else:
            messages.add_message(request, messages.ERROR, 'Login wrong')

    return render(request, "login.html")

def logout(request):

    ulogout(request)
    return redirect('index')
