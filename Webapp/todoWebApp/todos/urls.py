from django.urls import path
from .views import *

urlpatterns = [
    path('home', todaystodoTable, name='home_page'),
    path('', funcLogin, name="login_page"),
    path('register', funcRegister, name="register_page"),
    path('createTodo', createTodo, name='createTodo')
]
