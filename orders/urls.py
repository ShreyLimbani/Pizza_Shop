from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("home", views.home, name="home"),
    path("add-pizza", views.add_pizza, name="add_pizza"),
    path("place_order", views.place_order, name="place_order"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders")
]
