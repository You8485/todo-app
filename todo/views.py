from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
# Create your views here.
def user_login(request):
    context={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('todo:homepage')
        else:
            return render(request,'todo/login.html',{'error':'Enter Coreect Username or Password'})
    else:
        return render(request,'todo/login.html')

def registration(request):
    if request.method=='POST':
        form=userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            str="Enter Unique Email ID"
            try:
                user=User.objects.get(email=email)
                return render(request, 'todo/registration.html',{'form': form,'unique':str})
            except User.DoesNotExist:
                User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                return redirect('todo:login_url')
        else:
            str="User already exists change user name and try again"
            return render(request, 'todo/registration.html',{'form': form,'unique':str})
    else:
        form=userform()
        return render(request, 'todo/registration.html',{'form': form})

def index(request):
    print(request.user)
    #user=User.objects.get(username_id=request.user.username_id)
    task=Task.objects.filter(username_id=request.user)
    print(task)
    form=TaskForm()
    if request.method=="POST":
        form=TaskForm(request.POST)
        if form.is_valid():
            username_id=request.user
            title=form.cleaned_data['title']
            done=form.cleaned_data['done']
            obj=Task(username_id=username_id,title=title,done=done)
            obj.save()
            return redirect('todo:homepage')
    context={
        'tasks': task,
        'form' : form,
    }
    return render(request,'todo/task.html',context)

def update_task(request,pk):
    task=Task.objects.get(id=pk)
    form= TaskForm(instance=task)
    if request.method=="POST":
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:homepage')
    context={
        'form': form,
    }
    return render(request,'todo/up_task.html',context)

def delete_task(request,pk):
    task=Task.objects.get(pk=pk)
    if request.method=="POST":
        task.delete()
        return redirect('todo:homepage')
    context={
        'task': task,
    }
    return render(request,'todo/del_it.html',context)

def user_logout(request):
    logout(request)
    return redirect('todo:login_url')
