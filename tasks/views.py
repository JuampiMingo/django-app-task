from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.utils import timezone

from .forms import TaskForm
from .models import Task

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    context = {'form': UserCreationForm }
   
    if request.method == 'GET':
        return render(request, 'signup.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
           # register usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError: 
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password dont match'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html',{'tasks': tasks})



@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    context = {
        'form': AuthenticationForm
    }
    if request.method == "GET":
        return render(request, 'signin.html',context)
    else:
        
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html',context={
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

@login_required
def create_task(request):
    context = {
        'form': TaskForm 
        }
    if request.method == 'GET':
        
        return render(request, 'create_task.html',context)
    else:
        try:
          
            new_task = TaskForm(request.POST)
            task = new_task.save(commit=False)
            task.user = request.user
            task.save()
        
            return redirect('tasks')   
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error':'Please provide valid data'
            })

@login_required           
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{
        'task': task,
        'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            edit_task = TaskForm(request.POST, instance=task)
            edit_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', context={
                'task': task,
                'form': edit_task,
                'error': 'Error trying update task'
            })

@login_required # type: ignore
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required # type: ignore
def task_complete(request, task_id):
    pending_task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        pending_task.datecompleted = timezone.now()    
        pending_task.save()
        return redirect('tasks')   