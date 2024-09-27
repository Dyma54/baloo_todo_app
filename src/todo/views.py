from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import  messages

from .models import Todo
from .forms import TodoForm, RegisterForm, LoginForm

@login_required
def index(request):
    tasks = Todo.objects.filter(user=request.user)
    return render(request, template_name='todo/index.html', context={'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user=request.user
            task.save()
            messages.success(request, message='Votre tâche a bien été ajoutée.')
            return redirect(to='todo:index')
        else:
            messages.error(request, message="Impossible d'ajouter votre tâche")
            return render(request, template_name='todo/add-task.html', context={'form': form})

    form = TodoForm()
    return render(request, template_name='todo/add-task.html', context={'form': form})


@login_required
def modify_task(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, message='Votre tâche a bien été modifiée.')
            return  redirect(to='todo:index')
        else:
            messages.error(request, message='Votre formulaire contient une erreur.')
            return render(request, template_name='todo/modify-task.html', context={'form': form})

    form = TodoForm(instance=task)
    return render(request, template_name='todo/modify-task.html', context={'form': form})

@login_required
def remove(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, message='La tâche a bien été supprimée.')
        return redirect(to='todo:index')
    return render(request, template_name='todo/remove.html', context={'task': task})

def sign_up(request):
    if request.user.is_authenticated:
        messages.info(request, message="Vous êtes déjà connecté")
        return redirect(to='todo:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, message=f'Vous êtes connecté {user.username}. Soyez la bienvenue.')
            return redirect(to='todo:index')
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
            return render(request, template_name='todo/accounts/signup.html', context={'form': form})

    form = RegisterForm()
    return render(request, template_name='todo/accounts/signup.html', context={'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, message=f"Salut {user.username} ! Bienvenue.")
                return redirect('todo:index')
            else:
                messages.error(request, message=f"Votre email ou le mot de passe est incorrecte.")
                return render(request, template_name='todo/registration/login.html', context={'form': form})
        else:
            messages.error(request, message='Votre formulaire contient un problème.')
            return render(request, template_name='todo/registration/login.html', context={'form': form})
    form = LoginForm()
    return render(request, template_name='todo/registration/login.html', context={'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, message='Merci pour le temps que vous avez accordé à notre site aujourd’hui.')
    return redirect('login')

