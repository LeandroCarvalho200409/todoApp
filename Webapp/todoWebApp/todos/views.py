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
                    user = person.objects.create(username=username, password=str(dig_pwd), name=name+" "+surname, email=email)
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
        form = TodoForm(request.POST)
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
        form = TodoForm()
        return render(request, 'addTodo.html', {'form': form})

def alterTodo(request, name):
    change_todo_set = todo.objects.filter(name=name).all()
    change_todo = change_todo_set.first()
    current_data = {
        "name": change_todo.name,
        "text": change_todo.text,
        "date": change_todo.date,
        "done": change_todo.done,
    }

    if request.method == 'POST':
        print(current_data)
        form = TodoForm(request.POST, initial=current_data)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            text = form.cleaned_data['text']
            done = form.cleaned_data['done']

            change_todo.name = name
            change_todo.text = text
            change_todo.date = date
            change_todo.done = done
            change_todo.save()
            return redirect('home_page')
    else:
        form = TodoForm(initial=current_data)
        return render(request, 'alterTodo.html', {'form': form})


def setDone(request, name):
    todos_set = todo.objects.filter(name=name).all()
    doneTodo = todos_set.first()

    doneTodo.done = True
    doneTodo.save()
    return redirect('home_page')

def logout(request):
    user_set = person.objects.filter(id=request.session['user_id']).all()
    request.session['user_id'] = 0
    logout_user = user_set.first()
    logout_user.is_authenticated = False
    logout_user.save()
    return redirect('login_page')

def alterUser(request):
    change_person_set = person.objects.filter(id=request.session['user_id']).all()
    change_person = change_person_set.first()
    names = change_person.name.split(" ")
    current_data = {
        "name": names[0],
        'surname': names[1],
        "email": change_person.email,
        "username": change_person.username,
    }
    if request.method == "POST":
        form = RegisterForm(request.POST or None, initial=current_data)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            conf_pwd = form.cleaned_data['confirm_password']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            if password == conf_pwd:
                converted_pwd = hashlib.sha256(password.encode())
                dig_pwd = converted_pwd.hexdigest()
                change_person.name = name+" "+surname
                change_person.email = email
                change_person.password = str(dig_pwd)
                change_person.username = username
                change_person.save()
                return redirect("home_page")
            else:
                print("failed1")
                return render(request, "alterUser.html", {"form": form})
    else:
        form = RegisterForm(initial=current_data)
        return render(request, "alterUser.html", {"form": form})




#Tables
def todaystodoTable(request):
    today = date.today()

    user_id = request.session.get('user_id')
    print(user_id)

    today_date = today.strftime("%Y-%m-%d")
    print(today_date)
    todos_today = todo.objects.filter(person_fk_id=user_id, date=today_date, done=False).all()
    todos_future = todo.objects.filter(person_fk_id=user_id, date__gte=today, done=False).all()

    todos_today_count = todo.objects.filter(person_fk_id=user_id, date=today_date).count()
    todos_future_count = todo.objects.filter(person_fk_id=user_id, date__gte=today, done=False).count()

    context = {'todos_today': todos_today, 'todos_count': todos_today_count, 'todos_future': todos_future, 'todos_future_count': todos_future_count}
    return render(request, "home.html", context)
    

