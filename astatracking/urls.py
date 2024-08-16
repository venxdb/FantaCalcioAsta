# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'), 
    path('login/', views.login_view, name='login'),
    path('login/menu/', views.menu_view, name='menu'),
    path('login/menu/budget', views.budget_view, name = "budget"),
    path('login/menu/acquisti', views.acquisti_view, name = "acquisti")
]

