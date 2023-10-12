from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='appReservation.show'),
    path('create/', views.create, name='appReservation.create'),
    path('edit/<int:id>', views.edit, name='appReservation.edit'),
    path('update/<int:id>', views.update, name='appReservation.update'),
    path('delete/<int:id>', views.delete, name='appReservation.delete'),
]