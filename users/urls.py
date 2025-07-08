from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('handle_signup/', views.handle_signup, name="handle_signup"),
    path('handle_signin/', views.handle_signin, name='handle_signin'),
    path('cus_home/<str:username>', views.cus_home, name='cus_home'),
    path('admin_home/', views.admin_home, name='admin_home')
]