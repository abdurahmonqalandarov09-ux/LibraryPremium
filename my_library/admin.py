from django.contrib import admin
from .models import Books, Category, Authors, Publishers, Order

admin.site.register(Books)
admin.site.register(Category)
admin.site.register(Authors)
admin.site.register(Publishers)
admin.site.register(Order)