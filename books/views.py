from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, SigninForm, BookForm
from .models import Book, MyBook
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def buy_book(request, book_id):
    book_obj = Book.objects.get(id=book_id)
    if request.user.is_anonymous:
        return redirect('signin')
    
    buy = MyBook.objects.create(user=request.user, book=book_obj)
    return redirect('bought-books')

def booklist(request):
    query = request.GET.get('q')
    last_ten = Book.objects.all().order_by('-id')[:10]
    books = reversed(last_ten)
    if query:
        books = books.filter(
            Q(book_name__icontains=query)|
            Q(condition__icontains=query)|
            Q(isbn__icontains=query)|
            Q(author__icontains=query)
        ).distinct()


    context = {
       "books": books,

    }
    return render(request, 'list.html', context)
def bookdetail(request, book_id):
    book = Book.objects.get(id=book_id)


    context = {
        "book": book,
       
    }
    return render(request, 'detail.html', context)



def bought_books(request):
    if request.user.is_anonymous:
        return redirect('signin')
    book_list = request.user.mybook_set.all()
    context = {
        "book_list": book_list,
    }
    return render(request, 'bought_books.html', context)

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
            book = form.save(commit=false)
            book.owner = request.user
            book.save()
            return redirect('bought_books')

    context = {
        "form":form,
    }
    return render(request, 'create.html', context)

def book_delete(request, book_id):
    book_obj = Book.objects.get(id=book_id)
    # if not (request.user.is_staff):
    #     return redirect('no-access')
    book_obj.delete()
    return redirect('home')