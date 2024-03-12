"""
URL configuration for food_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentfication import views


from food.views import add_food, food_detail, food_list, get_foods_by_food_category, refresh_token
from food.views_food_category import delete_food_category, get_food_category, get_list_categories,add_food_category, update_food_category
from food.views_order import add_order, delete_one_orders, get_all_orders, get_one_order, update_order
from food.views_order_item import add_order_item, get_one_order_item, get_order_item_from_order, get_order_items
from food.views_restaurant import add_restaurant, delete_restaurant, get_list_restaurant, get_one_restaurant, update_restaurant

urlpatterns = [
    path('admin/', admin.site.urls),
    #auth
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('token/refresh',refresh_token),
    path('profil/', views.my_profil, name="logout"),

    #gestion des foods
    path('foods/', food_list),
    path('foods/add', add_food, name='add_food'),
    path('foods/category/<int:id>/', get_foods_by_food_category, name="get_foods_by_food_category"),
    path('foods/<int:pk>/', food_detail),

    #manage categories of food
    path('categories-foods/', get_list_categories, name="get_list_categories"),
    path('categories-foods/add/', add_food_category, name='add_category_food'),
    path('categories-foods/<int:id>/', get_food_category, name='get_food_category'),
    path('categories-foods/delete/<int:id>/', delete_food_category , name='delete_food_category'),
    path('categories-foods/update/<int:id>/', update_food_category, name='update_food_category'),

    #manage retaurant
    path('restaurants/', get_list_restaurant, name="get_list_restaurant"),
    path('restaurants/add/', add_restaurant, name="add_restaurant"),
    path('restaurants/<int:id>/', get_one_restaurant, name="get_one_restaurant"),
    path('restaurants/update/<int:id>/', update_restaurant, name="update_restaurant"),
    path('restaurants/delete/<int:id>/', delete_restaurant, name="delete_restaurant"),

    #manage order
    path('orders/', get_all_orders, name="get_all_orders"),
    path('orders/add/', add_order, name="add_order"),
    path('orders/<int:id>/', get_one_order, name="get_one_order"),
    path('orders/update/<int:id>/', update_order, name="update_order"),
    path('orders/delete/<int:id>/', delete_one_orders, name="delete_one_orders"),


    #manage item order
    path('orders-item/', get_order_items, name="get_order_items"),
    path('orders-item/add/', add_order_item, name="add_order_item"),
    path('orders-item/<int:id>/', get_one_order_item, name="get_one_order_item"),
    path('orders-item/order/<int:orderId>/', get_order_item_from_order, name="get_order_item_from_order"),
    #path('orders-item/delete/<int:id>/', delete_one_orders, name="delete_one_orders"),



]
