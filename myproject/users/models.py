from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, default=' ')
    middle_name = models.CharField(max_length=50, default=' ')
    last_name = models.CharField(max_length=50, default=' ')
    address = models.CharField(max_length=200, default=' ')
    pine_code = models.IntegerField(default=382481)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(default='M', max_length=6, choices=GENDER_CHOICES)
    mobile_no = models.PositiveBigIntegerField(default=9090656540)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'))
    message = models.CharField(default=' ', max_length=500)
    date_joined = models.DateTimeField(default=timezone.now)


class Category(models.Model):
    name = models.CharField(max_length=20, default="DISH")

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(default=' ', max_length=500)
    message = models.CharField(default=' ', max_length=500)
    date_joined = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(null=True, default=0,  blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        total = self.product.price * self.quantity
        return str(total)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    total = models.IntegerField(default=100)
    fname = models.CharField(max_length=10, default='name')
    lname = models.CharField(max_length=10, default='name')
    address = models.CharField(max_length=200, default='address')
    pinecode = models.IntegerField(default=382481)
    email = models.CharField(max_length=100, default='customer@gmail.com')
    mobile = models.PositiveBigIntegerField(default=9090656540)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
