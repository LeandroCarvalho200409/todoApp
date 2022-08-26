from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, FormView
from .models import person, todo
from .forms import *
from .tables import *
from .widget import DatePickerInput
import hashlib as hashlib
from datetime import date

# Normal Views and view functions


class HomePageView(ListView):
    model = todo
    template_name = 'home.html'
    context_object_name = 'all_todos_list'

def funcLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            converted_pwd = hashlib.sha256(password.encode())
            dig_pwd = converted_pwd.hexdigest()

            if person.objects.filter(username=username, password=str(dig_pwd)).values().count() >= 1:
                user = person.objects.filter(username=username, password=str(dig_pwd)).values()
                user.update(is_authenticated=True)
                first_user = user.first()
                request.session['user_id'] = first_user['id']
                return redirect('home_page')

    context = {'form': form}

    return render(request, "login.html", context)

def funcRegister(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            conf_pwd = form.cleaned_data['confirm_password']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']


            if person.objects.filter(username=username, email=email).values().count() == 0:
                if password == conf_pwd:
                    converted_pwd = hashlib.sha256(password.encode())
                    dig_pwd = converted_pwd.hexdigest()
                    user = person.objects.create(username=username, password=str(dig_pwd), name=surname+" "+name, email=email)
                    return redirect("home_page")
                else:
                    print("failed1")
                    return render(request, "register.html", {"form": form})
            else:
                print("failed2")
                return render(request, "register.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
    
def createTodo(request):
    if request.method == 'POST':
        form = AddTodoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            text = form.cleaned_data['text']
            done = form.cleaned_data['done']
            user_id = request.session['user_id']

            todos_found_nr = todo.objects.filter(name=name).values().count()
            print(todos_found_nr)

            if todos_found_nr == 0:
                newTodo = todo.objects.create(name=name, date=date, text=text, done=done, person_fk_id=user_id)
                return redirect('home_page')
            else:
                return render(request, 'addTodo.html', {'form': form})
    else:
        form = AddTodoForm()
        return render(request, 'addTodo.html', {'form': form})





#Tables
def todaystodoTable(request):
    today = date.today()

    user_id = request.session.get('user_id')
    print(user_id)

    today_date = today.strftime("%Y-%m-%d")
    print(today_date)
    table = TodaysTodoTable(todo.objects.filter(person_fk_id=user_id, date=today_date).all())

    context = {'table': table}
    return render(request, "home.html", context)
    

