from django.contrib import admin
from .models_item import Cart,DinnerPlatters,Orders ,ExtraForSubs,Meals ,Pasta, RegularPizza, Salad, SicilianPizza, Subs, Toppings
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.
admin.site.register(DinnerPlatters)
admin.site.register(ExtraForSubs)
admin.site.register(Pasta)
admin.site.register(Toppings)
admin.site.register(Subs)
admin.site.register(SicilianPizza)
admin.site.register(Salad)
admin.site.register(RegularPizza)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(Meals)
admin.site.register(User)
