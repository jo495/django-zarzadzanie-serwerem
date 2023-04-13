from django.urls import path
from . import views

app_name = 'cloudpilot'

urlpatterns = [
    path('', views.button_list, name='button_list'),
    path('<int:id>/', views.turn_on),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('logout/', views.logoutPage, name='logoutPage'),
]