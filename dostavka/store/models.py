from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ROLE_CHOICES=(
        ('Administrator','Administrator'),
        ('Owner', 'Owner'),
        ('client', 'client'),
        ('Courier', 'Courier'),
    )
    user_role=models.CharField(max_length=16, choices=ROLE_CHOICES, default='client')
    phone_number=PhoneNumberField(null=True, blank=True)


class Category(models.Model):
    category_name=models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Store(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_name=models.CharField(max_length=64)
    description=models.TextField(null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='store_category')
    address=models.CharField(max_length=100)
    image = models.ImageField(upload_to='img/',)


    def __str__(self):
        return self.store_name

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.stars or 0 for i in ratings) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        ratings = self.reviews.all()
        if ratings.exists():
            if ratings.count() > 3:
                return f'3+'
            elif ratings.count():
                return ratings.count()
        return 0



class Contacts(models.Model):
    store=models.ForeignKey(Store, related_name='contacts', on_delete=models.CASCADE)
    contact_info=PhoneNumberField()


class Product(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product_name


class Combo(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.PositiveSmallIntegerField()
    store=models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_combo')

    def __str__(self):
        return self.product_name


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews',)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг",)
    text=models.TextField(null=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    datetime=models.DateTimeField(auto_now_add=True)


class CourierReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='rating')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='courier_reviews',)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг",)
    text=models.TextField(null=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    datetime=models.DateTimeField(auto_now_add=True)


class ProductsCart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'


class ProductsItem(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ProductsCart, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.user}, {self.post}'


class Order(models.Model):
    client=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client')
    cart=models.ForeignKey(ProductsItem, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Ожидает обработки','Ожидает обработки'),
        ('В процессе доставки', 'В процессе доставки'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
    )
    status=models.CharField(max_length=32, choices=STATUS_CHOICES, default='Ожидает обработки')
    address=models.CharField(max_length=100)
    courier=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.status}, {self.courier}'


class Courier(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier')
    current_orders=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    TYPE_STATUS_CHOICES=(
        ('занят' ,'занят'),
        ('доступен','доступен')
    )
    status=models.CharField(max_length=32, choices=TYPE_STATUS_CHOICES)

    def __str__(self):
        return f'{self.user}, {self.status}'


