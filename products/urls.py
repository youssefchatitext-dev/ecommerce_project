from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('<int:id>/', views.product_detail, name="product_detail"),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
<<<<<<< HEAD
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
]
=======
]
>>>>>>> f81f612207979a3dec3531f73deb3ea7a70a8c73
