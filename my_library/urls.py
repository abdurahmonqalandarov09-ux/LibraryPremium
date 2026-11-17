from django.urls import path
from .views import *

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('registration/', register, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('book/<int:id>/', book_page, name='book_page'),
    path('create_book/', create_book, name='create_book'),
    path('show_books/', show_book, name='show_books'),
    path('update_book/<int:id>/', update_book, name='update_book'),
    path('delete_book/<int:id>/', delete_book, name='delete_book'),
    path('order_book/<int:id>/', order_book, name='order_book'),
    path('my_orders/', my_orders, name='my_orders')
] 
