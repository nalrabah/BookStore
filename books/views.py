from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, SigninForm, BookForm
from .models import Book
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def booklist(request):
    books = Book.objects.all()
    context = { "books": books}
    return render(request, 'list.html', context)

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            query = User.objects.filter(email=user.email)
            if query:
                messages.info(request,"This email is already registered")

            else:
                user.username = user.email
                user.set_password(user.password)
                user.save()

                login(request, user)
                return redirect("book-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=email, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('book-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")

def book_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)