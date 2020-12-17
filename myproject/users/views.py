from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import CreateView, View
from .forms import CustomUserCreationForm, ContactForm, CustomUserChangeForm, FeedbackForm
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views import generic
from .tokens import account_activation_token
from django.core.mail import EmailMessage

def home(request):
    return render(request, 'index.html')


def register(req):
    form = CustomUserCreationForm(req.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(req)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return redirect('msg')
    form = CustomUserCreationForm()
    return render(req, 'register.html', {'form': form})





    # if req.method == 'POST':
    #     form = CustomUserCreationForm(req.POST)
    #     if form.is_valid():
    #         form.save()
    #         subject = 'Customer Varifications'
    #         message = 'Thank You for the Registration. Welcome to FoodFunday Restaurant. Click this link for the Login. http://127.0.0.1:8000/accounts/login/    '
    #         recipient = form.cleaned_data.get('email')
    #         send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    #         messages.success(req, 'Success!')
    #         return redirect('msg')
    # return render(req, 'register.html', {'form': form})


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        return render(request, 'activation_failed.html', status=401)


def msg(req):
    return render(req, 'msg.html')


class edit_profile(generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


def profile(request):
    return render(request, 'profile.html')


class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')


def feedback(req):
    form = FeedbackForm()
    data = Feedback.objects.all()
    if req.method == 'POST':
        form = FeedbackForm(req.POST)
        form.save()
        return redirect('feedback')
    return render(req, 'feedback.html', {'form': form, 'data': data})


def category(request):
    menu = category.objects.all()
    return render(request, 'category.html', {'menu': menu})


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return CustomUserCreationForm.login(request, *args, **kwargs)


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.objects.all().filter(category_id=categoryID)
    else:
        products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'category': category}
    return render(request, 'store.html', context)


def bill(request):
    data = cartData(request)
    cartItems = data['cartItems']
    customer = request.user.customer
    id = customer.id
    order = Order.objects.filter(customer_id=id)
    items = []
    for o in order:
        items += OrderItem.objects.all().filter(order=o)

    return render(request, 'bill.html', {'items': items, 'cartItems': cartItems})


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


# @login_required(login_url='login')
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def order(request):
    if request.method == "post":
        pro_name = request.POST["p_name"]
        pro_price = request.POST["p_price"]
        qty = request.POST["quantity"]
        t_item = request.POST["t_item"]
        total = request.POST["total"]
    return render(request, 'checkout.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.total = (orderItem.total + orderItem.product.price)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.total = (orderItem.total - orderItem.product.price)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.total = total
    order.save()

    Bill.objects.create(
        customer=customer,
        order=order,
        total=total,
        fname=data['shipping']['fname'],
        lname=data['shipping']['lname'],
        address=data['shipping']['address'],
        pinecode=data['shipping']['pinecode'],
        email=data['shipping']['email'],
        mobile=data['shipping']['mobile'],
        )
    if request.user.is_authenticated:
        email = request.user.customer.email
        subject = 'Food Funday Order Details'
        message = f'Hello, Welcome to FoodFunday Restaurant. Thank you for your order!!! Your food is being made soon!!!  Your total: "{total}". Thank you again for your order : )'
        recipient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

    return JsonResponse('Payment submitted..', safe=False)
