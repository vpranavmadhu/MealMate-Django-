from django.urls import path
from . import views

app_name="delivery"
urlpatterns = [
    path('add_res/', views.add_res, name='add_res'),
    path('veiw_menu/<int:id>/',views.view_menu, name="view_menu"),
    path('add_menu/',views.add_menu, name='add_menu'),
    path('delete_menu/<int:id>', views.delete_menu, name='delete_menu'),
    path('view_cusmenu/<int:id>/<str:username>/',views.view_cusmenu, name="view_cusmenu"),
    path('view_cart/<str:username>/', views.view_cart, name="view_cart"),
    path('add_to_cart/<int:menuid>/<str:username>/', views.add_to_cart, name="add_to_cart"),
    path('ordersucess/<str:username>', views.ordersucess, name="ordersucess"),
    path('orders/<str:username>',views.orders,name='view_orders'),
    path('edit_res/<int:id>', views.edit_res,name="edit_res"),
    path('delete_res/<int:id>', views.delete_res,name="delete_res"),
    path('edit_menu/<int:id>', views.edit_menu,name="edit_menu"),
    path('cart/quantity/<int:id>/<str:op>/', views.cart_quantity, name='cart_quantity'),

]