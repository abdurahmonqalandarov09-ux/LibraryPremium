from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Books, Category, Authors, Publishers, Order



def is_admin(user):
    return user.is_staff





def register(request):
    if request.method == "POST":
        data = request.POST
        if data:
            User.objects.create_user(
                username = data['username'],
                password = data['password']
            )
    else: 
        return redirect('home')
    return render(request, 'registration.html')




def login_user(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(request, username = data['username'], password = data['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')
    return render(request, 'login.html')



@login_required
def logout_user(request):
    logout(request)
    return redirect('login')




@login_required
def profile(request):
    return render(request, 'profile.html')



@login_required
def home(request):
    books = Books.objects.filter(is_active=True).order_by('?')[:6]
    return render(request, 'home_page.html', {'books': books})



@login_required
def search(request):
    q = request.GET.get('q', '')
    books = Books.objects.filter(title__icontains = q, is_active = True)
    return render(request, 'search.html', {'books': books, 'q': q})

@login_required
def book_page(request, id):
    book = get_object_or_404(Books, id=id)
    return render(request, 'book_page.html', {'book': book})


@login_required
def order_book(request, id):
    book = get_object_or_404(Books, id=id)
    if request.method == 'POST' and book.stock > 0:
        order = Order.objects.create(user = request.user)
        order.books.add(book)
        book.stock -= 1
        book.save()
    return redirect('my_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, 'my_orders.html', {'orders': orders})




@user_passes_test(is_admin, login_url='login')
def create_book(request):
    if request.method == "POST":
        data = request.POST
        book = Books.objects.create(
            title=data['title'],
            caption=data['caption'],
            price=data['price'],
            stock=data['stock'],
            content=data['content'],
            picture=request.FILES.get('picture'),
            video=request.FILES.get('video'),
            publisher_id=data['publisher'],
        )
        book.categories.set(data.getlist('categories'))
        book.authors.set(data.getlist('authors'))
        return redirect('home')
    return render(request, 'create_book.html', {
        'categories': Category.objects.all(),
        'authors': Authors.objects.all(),
        'publishers': Publishers.objects.all(),
    })




@user_passes_test(is_admin, login_url='login')
def show_book(request):
    if request.method == "GET":
        books = Books.objects.all()
        return render(request, 'show_book.html', {'books': books})





@user_passes_test(is_admin, login_url='login')
def update_book(request, id):
    book = get_object_or_404(Books, id=id)
    if request.method == "POST":
        data = request.POST
        book.title = data['title']
        book.caption = data['caption']
        book.price = data['price']
        book.stock = data['stock']
        book.content = data['content']
        book.publisher_id = data['publisher']
        if request.FILES.get('picture'):
            book.picture = request.FILES['picture']
        if request.FILES.get('video'):
            book.video = request.FILES['video']
        book.save()
        book.categories.set(data.getlist('categories'))
        book.authors.set(data.getlist('authors'))
        return redirect('show_books')
    return render(request, 'update_book.html', {
        'book': book,
        'categories': Category.objects.all(),
        'authors': Authors.objects.all(),
        'publishers': Publishers.objects.all(),
    })



@user_passes_test(is_admin, login_url='login')
def delete_book(request, id):
    book = get_object_or_404(Books, id=id)
    if request.method == "POST":
        book.delete()
        return redirect('show_books')
    return render(request, 'delete_book.html', {'book': book})




