from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
import sys
import json
from django.shortcuts import render
from .models_item import Meals, Cart,Orders, RegularPizza,SicilianPizza,Subs,DinnerPlatters,Pasta,Salad,Toppings
from django.core import serializers
from django.contrib.auth import login, logout, authenticate,get_user_model
# Create your views here.
User = get_user_model()
#when users go to the defult route , run this function
def index(request):
    if request.user.is_authenticated:
        try:
            #if customers have some meal in cart then try to load this
            myorders = Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all()
        except:
            #if customers do not have any meals in Cart
            myorders = None

        #all meals will appear on the menu
        context = {
            "RPs":RegularPizza.objects.all(),
            "SPs":SicilianPizza.objects.all(),
            "Subs":Subs.objects.all(),
            "DPs":DinnerPlatters.objects.all(),
            "Pastas":Pasta.objects.all(),
            "Salads":Salad.objects.all(),

            "incarts":myorders,
            "login":"login",
            "user":request.user,
        }
        return render(request, "orders/menu.html",context)
    else:
        return render(request, "orders/login.html")

#add order to Cart tsble
def addtocart(request):
    #these will be used to add order to Cart in database
    className = request.POST["className"]
    order_id = request.POST["order_id"]
    size = request.POST["size"]

    try :
        #if user profile exists in Cart table
        order = Cart.objects.get(customer=User.objects.get(email = request.user.email))
    except:
        #if user profile does not exist in Cart table, then create a new Cart row for user
        order = Cart(customer=User.objects.get(email = request.user.email))
    #save it to make operation for it available
    order.save()


    #convert string to class to query (class name from javascript send to server as string)
    className1 = getattr(sys.modules[__name__], className)

    #create meal to add cart and order for users' interest
    meal = Meals(order=className1.objects.get(pk=order_id),price=size)

    meal.save()

    #it will add toppings to RegularPizza or SicilianPizza
    if className == 'RegularPizza' or className == 'SicilianPizza':
        toppings = request.POST["toppings"]
        toppings = toppings.split(',')
        for topping in toppings:
            meal.toppings.add(Toppings.objects.get(pk=int(topping)))

    #meal is being added to order colomn in Cart
    order.order.add(meal)

    #orders will be all orders, in Cart, of user loged in
    orders = Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all()
    #make those information json object to work on,after sending to client side with Ajax, in javascript
    orders = serializers.serialize('json',orders)

    #meals will have name of all orders to show clients what they have ordered or just make user friendly.
    meals = []
    for meal in Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all():
        meals.append(meal.order)

    #make those information json object to work on,after sending to client side with Ajax, in javascript
    meals = serializers.serialize('json',meals)

    #return these to show users what they have added to cart
    return JsonResponse({"meals":meals,"orders":orders},safe=False)

#add orders to Order table and remove from Cart table When users want to order
def order(request):
    #what user has in Cart table (class)
    mycarts = Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all()
    try:
        #if user profile exists in Order table
        myorders = Orders.objects.get(customer=User.objects.get(email = request.user.email))
    except:
        #create a new Order row for user
        myorders = Orders(customer=User.objects.get(email = request.user.email))
    myorders.save()

    #transfer all meals from Cart to Order database, it means user confirmed
    for meal in mycarts:
        myorders.order.add(Meals.objects.get(pk=meal.pk))

    #delete orders from Cart database
    Cart.objects.get(customer=User.objects.get(email = request.user.email)).delete()
    #return what user ordered
    return HttpResponse(Orders.objects.get(customer=User.objects.get(email = request.user.email)))

#remove order from Cart table, if users do not want to order
def removeItem(request):
    try:
        #pk is id of meal, in Meals table, wanted to remove from Cart table
        pk=int(request.POST["pk"])

        #meal i limit li etsen # QUESTION: Meals.objects.delete() deyis
        #remove meal from Meals table wantet to remove
        Meals.objects.get(pk=pk).delete()

        #orders will be all orders, in Cart, of user loged in
        orders = Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all()

        #make those information json object to work on,after sending to client side with Ajax, in javascript
        orders = serializers.serialize('json',orders)

        #meals will have name of all orders to show clients what they have ordered or just make user friendly.
        meals = []
        for meal in Cart.objects.get(customer=User.objects.get(email = request.user.email)).order.all():
            meals.append(meal.order)

        #make those information json object to work on,after sending to client side with Ajax, in javascript
        meals = serializers.serialize('json',meals)

        #return meal to show users currently what they have in Cart table
        return JsonResponse({"meals":meals,"orders":orders},safe=False)
    except:
        #raise an Exception for any type of error
        raise Exception("Error occured")

def render_login(request):
    return render(request, "orders/login.html")

def login_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request,username=email,password=password)

    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse(email)

def load_toppings(request):
    toppings = serializers.serialize('json',Toppings.objects.all())
    return JsonResponse({"topping":toppings},safe=False)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def render_signup(request):
    return render(request, "orders/signup.html")

def signup(request):
    email = request.POST['email']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user = User.objects.create_superuser(email,password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return HttpResponseRedirect(reverse('render_login'))
