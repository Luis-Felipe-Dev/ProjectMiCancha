from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='appEstablishment.show'),
    path('create/', views.create, name='appEstablishment.create'),
    path('edit/<int:id>', views.edit, name='appEstablishment.edit'),
    path('update/<int:id>', views.update, name='appEstablishment.update'),
    path('delete/<int:id>', views.delete, name='appEstablishment.delete'),
]