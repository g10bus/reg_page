from django.shortcuts import render,redirect
from django.http import HttpResponse


def registerPage(request):
    return render(request,"register.html",)

def homePage():
    pass

def loginPage():
    pass

def profilePage():
    pass