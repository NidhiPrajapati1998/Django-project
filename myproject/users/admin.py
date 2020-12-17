from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id', 'total')
    list_per_page = 6
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added', 'total')
    list_per_page = 10
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'image')
    list_per_page = 10
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 10
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')
    list_per_page = 10
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message', 'date_joined')
    list_per_page = 10
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'message', 'date_joined')
    list_per_page = 10
    pass


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'total', 'fname', 'lname', 'address', 'pinecode', 'email', 'mobile', 'date_added')
    list_per_page = 10
    pass


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Create view
    form = CustomUserChangeForm  # Update view
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', "first_name", "middle_name", "last_name", "address", "pine_code", "mobile_no", "gender",)
    list_filter = ('email', 'is_staff', 'is_active', "first_name", "middle_name", "last_name", "address", "pine_code", "mobile_no", "gender", )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ("first_name", "middle_name", "last_name", "address", "pine_code", "mobile_no", "gender",)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
