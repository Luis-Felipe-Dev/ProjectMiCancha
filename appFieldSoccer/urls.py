from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='appFieldSoccer.show'),
    path('create/', views.create, name='appFieldSoccer.create'),
    path('edit/<int:id>', views.edit, name='appFieldSoccer.edit'),
    path('update/<int:id>', views.update, name='appFieldSoccer.update'),
    path('delete/<int:id>', views.delete, name='appFieldSoccer.delete'),
]