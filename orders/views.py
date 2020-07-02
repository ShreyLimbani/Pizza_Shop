from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from orders.models import Pizza, Topping, Order, Status
from django.views.decorators.http import require_http_methods


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html", {"message": None})
    return HttpResponseRedirect(reverse("home"))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/index.html", {"message": "Invalid credentials."})


@login_required
def logout_view(request):
    logout(request)
    return render(request, "orders/index.html", {"message": "Logged out."})


def register_view(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    try:
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                        password=password)
        user.save()
        return HttpResponseRedirect(reverse("index"))
    except:
        return render(request, "orders/index.html", {"message": "Invalid credentials."})


@login_required
def home(request):
    pizzas = Pizza.objects.all()
    toppings = Topping.objects.all()
    try:
        cart_orders_count = Order.objects.filter(user_id=request.user, status=3).count()
        # Status 1 is Pending, Status 2 is Completed, Status 3 is Cart
    except Order.DoesNotExist:
        cart_orders_count = 0
    context = {
        "pizzas": pizzas,
        "orders": cart_orders_count,
        "toppings": toppings
    }

    return render(request, "orders/home.html", context)


@login_required
@require_http_methods(["POST"])
def add_pizza(request):
    order = Order.objects.create(user_id=request.user,
                                 pizza=Pizza.objects.get(pk=request.POST['pizza_id']),
                                 size=request.POST['pizza_size'],
                                 price=request.POST['pizza_total'],
                                 status=Status.objects.get(pk=3))
    toppings = set()
    if request.POST['pizza_toppings'] != '0':
        pizza_toppings = request.POST['pizza_toppings'].split(',')
        for topping_id in pizza_toppings:
            toppings.add(Topping.objects.get(pk=topping_id))
        order.toppings.set(toppings)
    print(toppings)

    return JsonResponse({"success": True})


def cart(request):
    try:
        cart_orders = Order.objects.filter(user_id=request.user, status=3)
        cart_orders_count = cart_orders.count()
        # Status 2 is Completed and status 1 is pending
    except Order.DoesNotExist:
        cart_orders_count = 0
    context = {
        'cart_orders': cart_orders,
        'cart_orders_count': cart_orders_count
    }
    return render(request, "orders/cart.html", context)


@login_required
@require_http_methods(["POST"])
def place_order(request):
    order_ids = request.POST['current_order_ids'].split(',')
    for order_id in order_ids:
        order = Order.objects.get(pk=order_id)
        order.status = Status.objects.get(pk=1)
        order.save()

    return JsonResponse({"success": True})


@login_required
def orders(request):
    try:
        user_orders = Order.objects.filter(Q(user_id=request.user, status=1) | Q(user_id=request.user, status=2))
        orders_count = user_orders.count()
        cart_orders_count = Order.objects.filter(user_id=request.user, status=3).count()

        # Status 1 is Pending, Status 2 is Completed, Status 3 is Cart

    except Order.DoesNotExist:
        cart_orders_count = 0
    context = {
        'orders': user_orders,
        'orders_count': orders_count,
        'cart_orders_count': cart_orders_count
    }
    return render(request, "orders/orders.html", context)
