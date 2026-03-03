from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User


# def redir(request):
#   return redirect('register',permanent=True)

def registerPage(request):
    if request.POST:
        # Запись данных в бд

        User.objects.create(email = request.POST["email"],
                            first_name = request.POST["firstname"],
                            last_name = request.POST["surname"],
                            middle_name = request.POST["middleName"],
                            password = request.POST["password"])
        #Пароль нужно хэшировать
        return redirect('profile')

    return render(request,"register.html",)

def homePage():
    pass

def loginPage():
    pass

def profilePage(request):
    data = User.objects.get(pk = 3)

    return render(request, "profile.html", {"data": data } )