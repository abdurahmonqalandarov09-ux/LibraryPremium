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



@user_passes_test(is_admin, login_url='login')
def add_category(request):
    if request.method == "POST":
        data = request.POST
        Category.objects.create(
            category_name = data['category_name']
        )
        return redirect('show_categories')
    return render(request, 'add_category.html')



@user_passes_test(is_admin, login_url='login')
def show_categories(request):
    if request.method == "GET":
        category = Category.objects.all()
        return render(request, 'show_category.html', {'category': category})



@user_passes_test(is_admin, login_url='login')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.category_name = request.POST['category_name']
        category.save()
        return redirect('show_categories')
    return render(request, 'update_category.html', {'category': category})




@user_passes_test(is_admin, login_url='login')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect('show_categories')
    return render(request, 'delete_category.html', {'category': category})






@user_passes_test(is_admin, login_url='login')
def create_author(request):
    if request.method == "POST":
        data = request.POST
        Authors.objects.create(
            name = data['name'],
            age = data['age'],
            country = data['country']
        )
        return redirect('show_authors')
    return render(request, 'create_author.html')



@user_passes_test(is_admin, login_url='login')
def show_author(request):
    if request.method == "GET":
        author = Authors.objects.all()
        return render(request, 'show_author.html', {'author': author})



@user_passes_test(is_admin, login_url='login')
def update_author(request, id):
    author = get_object_or_404(Authors, id=id)
    if request.method == "POST":
        data = request.POST
        author.name = data['name']
        author.age = data['age']
        author.country = data['country']
        author.save()
        return redirect('show_authors')
    return render(request, 'update_author.html', {'author': author})



@user_passes_test(is_admin, login_url='login')
def delete_author(request, id):
    author = get_object_or_404(Authors, id=id)
    if request.method == "POST":
        author.delete()
        return redirect('show_authors')
    return render(request, 'delete_author.html', {'author': author})




@user_passes_test(is_admin, login_url='login')
def create_publisher(request):
    if request.method == "POST":
        data = request.POST
        Publishers.objects.create(
            publisher_name = data['publisher_name']
        )
        return redirect('show_publishers')
    return render(request, 'create_publisher.html')




@user_passes_test(is_admin, login_url='login')
def show_publisher(request):
    if request.method == "GET":
        publisher = Publishers.objects.all()
        return render(request, 'show_publisher.html', {'publisher': publisher})






@user_passes_test(is_admin, login_url='login')
def update_publisher(request, id):
    publisher = get_object_or_404(Publishers, id=id)
    if request.method == "POST":
        data = request.POST
        publisher.publisher_name = data['publisher_name']
        publisher.save()
        return redirect('show_publishers')
    return render(request, 'update_publisher.html', {'publisher': publisher})




@user_passes_test(is_admin, login_url='login')
def delete_publisher(request, id):
    publisher = get_object_or_404(Publishers, id=id)
    if request.method == "POST":
        publisher.delete()
        return redirect('show_publishers')
    return render(request, 'delete_publisher.html', {'publisher': publisher})