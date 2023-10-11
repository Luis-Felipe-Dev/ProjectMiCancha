from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='appUser.show'),
    path('create/', views.create, name='appUser.create'),
    path('edit/<int:id>', views.edit, name='appUser.edit'),
    path('update/<int:id>', views.update, name='appUser.update'),
    path('delete/<int:id>', views.delete, name='appUser.delete'),
    path('reset_password/<int:id>', views.reset_password, name='appUser.reset_password'),
    path('search/', views.search, name='appUser.search'),
]