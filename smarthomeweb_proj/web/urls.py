from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("sensors/", views.display_sensors),
    path("sensors/temps", views.display_temps),
    path("sensors/temps/<str:temp_id>/", views.display_temps, name="temp_detail"),
    path("sensors/air-press/", views.display_air_press, name="temp_detail"),
    path("sensors/humid", views.display_humid),
    path("sensors/new/", views.new_sensor),
    path('sensors/edit/<str:sensor_id>/', views.edit_sensor),

    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.user_login, name='login'),
    path('auth/logout/', views.user_logout, name='logout'),
]
