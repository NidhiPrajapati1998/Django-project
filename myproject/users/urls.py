from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('msg/', views.msg, name='msg'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profile/', views.profile, name='profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('edit_profile', edit_profile.as_view(), name='edit_profile'),
    path("password/", auth_views.PasswordChangeView.as_view(template_name='password_change.html')),
    path("accounts/password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('bill/', views.bill, name="bill"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path("activate/<uidb64>/<token>", views.ActivateAccountView.as_view(), name='activate'),
]
