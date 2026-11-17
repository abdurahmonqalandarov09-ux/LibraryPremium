from django.db import models
from django.contrib.auth.models import User






class Category(models.Model):
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return self.category_name
    



class Publishers(models.Model):
    publisher_name = models.CharField(max_length=120)


    def __str__(self):
        return self.publisher_name






class Authors(models.Model):
    name = models.CharField(max_length=120)
    age = models.PositiveBigIntegerField()
    country = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class Books(models.Model):
    title = models.CharField(max_length=120)
    caption = models.TextField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveBigIntegerField(default=0)
    categories = models.ManyToManyField(Category)
    authors = models.ManyToManyField(Authors)
    picture = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/', blank=True)
    content = models.TextField(max)
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = [
        ('available', 'Доступный'),
        ('unavailable', 'Не доступен')
    ]
    books = models.ManyToManyField(Books)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    
    

    