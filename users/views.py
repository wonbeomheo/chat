from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from rest_framework.authtoken.models import Token


def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list,
               'user': request.user, }
    token_key = request.COOKIES['Login-Token']
    try:
        user_id = Token.objects.get(key=token_key).user_id
        user = User.objects.get(id=user_id)
        context['message'] = user.username
    except Token.DoesNotExist:
        pass
    return render(request, 'base.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            Token.objects.get_or_create(user=user)
            login(request, user=user)
            context = {'message': user.username + ' You logged in successfully.'}
            response = render(request, 'users/signin.html', context)
            response.set_cookie('Login-Token', Token.objects.get(user=user).key)
            return response
        else:
            messages.error(request, 'ID or Password was incorrect.')
            return redirect('users:signin')
    else:
        return render(request, 'users/signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['re-password']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('users:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered.")
            return redirect('users:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('users:signup')

        user = User.objects.create_user(username, email, pass1)
        user.save()
        messages.success(request, "Your account has been successfully created.")

        return redirect('users:signin')
    else:
        return render(request, 'users/signup.html')


def signout(request):
    Token.objects.filter(user=request.user).delete()
    logout(request)
    response = redirect('users:home')
    response.set_cookie('Login-Token', '')
    messages.success(request, "Logged Out Successfully.")
    return response
