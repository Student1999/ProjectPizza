from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addtocart",views.addtocart, name="addtocart"),
    path("order", views.order, name="order"),
    path("removeItem",views.removeItem,name="removeItem"),
    path("load_toppings",views.load_toppings,name="load_toppings"),

    path("render_login",views.render_login,name="render_login"),
    path("login_view",views.login_view,name="login_view"),
    path("logout",views.logout_view, name="logout"),
    path("render_signup",views.render_signup, name="render_signup"),
    path("signup",views.signup, name="signup"),

]
