from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate,login,logout


def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user = User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/loginn')

    return render(request, 'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)
        user = authenticate(request, username =fnm, password = pwd)
        if user is not None:
            login(request,user)
            return redirect('/todopage')
        else:
            return redirect('/loginn')

    return render(request,'loginn.html')

def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj = models.TODOO(title=title,user= request.user)
        obj.save()
    return render(request,'todo.html')