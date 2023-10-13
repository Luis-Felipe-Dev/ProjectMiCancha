from django.urls import path
from . import views

urlpatterns = [
    path('', views.show, name='appReservation.show'),
    path('create/', views.create, name='appReservation.create'),
    path('edit/<int:id>', views.edit, name='appReservation.edit'),
    path('update/<int:id>', views.update, name='appReservation.update'),
    path('delete/<int:id>', views.delete, name='appReservation.delete'),
    path('get_establishment/<int:type_dist_id>/', views.get_establishment, name='get_establishment'),
    path('get_field_soccer/<int:establishment_id>/', views.get_field_soccer, name='get_field_soccer'),
]