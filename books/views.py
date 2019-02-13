from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, SigninForm, BookForm
from .models import Book
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def booklist(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(book_name__icontains=query)|
            Q(condition__icontains=query)|
            Q(isbn__icontains=query)|
            Q(author__icontains=query)
        ).distinct()

    # favorite_list = []
    # if request.user.is_authenticated:
    #     favorite_list = request.user.favoriterestaurant_set.all().values_list('restaurant', flat=True)

    context = {
       "books": books,
       # "favorite_list": favorite_list
    }
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