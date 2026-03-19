from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User
import os, hashlib, secrets

# def redir(request):
#   return redirect('register',permanent=True)

def registerPage(request):
    if request.POST:
        # Запись данных в бд
        password = request.POST["password"].encode()
        salt = os.urandom(16)
        hash_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)


        user = User.objects.create(email = request.POST["email"],
                            first_name = request.POST["firstname"],
                            last_name = request.POST["surname"],
                            middle_name = request.POST["middleName"],
                            password = hash_password.hex(),
                            salt_password = salt.hex())

        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        return redirect('profile')

    return render(request,"register.html",)


def loginPage(request, a=False):
    if request.method == 'POST':
        email_get = request.POST["email"]
        password_get = request.POST["password"].encode()

        try:
            user = User.objects.get(email=email_get)
            hash_user_password = user.password
            user_password_salt = bytes.fromhex(user.salt_password)

            hash_get_password = hashlib.pbkdf2_hmac('sha256', password_get, user_password_salt, 100000)

            if secrets.compare_digest(hash_user_password, hash_get_password.hex()):
                # СОХРАНЯЕМ ID В СЕССИИ вместо передачи в URL
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                # Можно сохранить и другие данные

                return redirect('profile')  # БЕЗ ID в URL!
            else:
                a = True
        except User.DoesNotExist:
            a = True

    return render(request, "login.html", {"a": a})


def logoutPage(request):

    request.session.flush()
    return redirect('login')

def profilePage(request):
    # Получаем ID пользователя из сессии (не из URL!)
    user_id = request.session.get('user_id')

    message = None

    # Проверяем, есть ли пользователь в сессии
    if not user_id:
        return redirect('login')  # Если нет - на логин

    if request.method == "POST":
        password_get = request.POST["current_password"].encode()
        print(request.POST)

        user = User.objects.get(id=user_id)

        hash_user_password = user.password
        user_password_salt = bytes.fromhex(user.salt_password)

        hash_get_password = hashlib.pbkdf2_hmac('sha256', password_get, user_password_salt, 100000)

        if secrets.compare_digest(hash_user_password, hash_get_password.hex()):
            message = "COR"

            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.middle_name = request.POST["middle_name"]
            user.phone = request.POST["phone"]


            if request.POST["new_password"]:
                new_password = request.POST["new_password"].encode()
                hash_new_password = hashlib.pbkdf2_hmac('sha256', new_password, user_password_salt, 100000)
                user.password = hash_new_password.hex()

            user.save()

        else:
            message = "ENCR"



    try:
        data = User.objects.get(pk=user_id)
        return render(request, "profile.html", {"data": data, "message":message})

    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')




