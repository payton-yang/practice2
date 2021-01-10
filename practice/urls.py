"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from users import views as user_view
from products import views as product_view
from carts import views as cart_view
from orders import views as order_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', user_view.UserList.as_view()),
    path('users/<int:pk>/', user_view.UserDetail.as_view()),
    path('login/', user_view.Login.as_view()),
    path('products/', product_view.ProductList.as_view()),
    path('products/<int:pk>/', product_view.ProductDetail.as_view()),
    path('carts/<int:pk>/', cart_view.CartDetail.as_view()),
    path('orders/', order_view.Order.as_view()),

]
