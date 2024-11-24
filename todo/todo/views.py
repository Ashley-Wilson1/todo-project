from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

#this function handles to signup request sends user to login page
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

#this function handles to login sends user to todo page
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

#this handles to tasks that user adds
@login_required(login_url='/loginn')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj = models.TODOO(title=title,user= request.user)
        obj.save()
        user=request.user
        res = models.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage',{'res':res})
    
    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res':res})

#this handles the user deleting a task
@login_required(login_url='/loginn')
def delete_todo(request,srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

#this handles the page that the user uses to edit a task
@login_required(login_url='/loginn')
def edit_todo(request,srno):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj = models.TODOO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        return redirect('/todopage')
    
    obj = models.TODOO.objects.get(srno=srno)
    return render(request,'edit_todo.html',{'obj':obj})

#handles the sign out
def signout(request):
    logout(request)
    return redirect('/loginn')
    