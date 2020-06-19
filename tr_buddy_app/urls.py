from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.create_user), #PASS 
    path('',views.login), #PASS index-login-login(fun)
    path('login', views.login), #PASS validates login
    path('dashboard', views.dashboard),
    path('log_out', views.log_out),
    path('delete/<int:id>', views.delete),
    path('trips/new', views.add_trip_page),
    path('create_trip', views.create_trip),
    path('trips/<int:id>/destroy', views.delete),
    path('trips/edit/<int:id>', views.editpage), 
    path('trips/update/<int:id>', views.edit_trip), 
    path('trips/<int:id>', views.trip_info),
    path('trip_info/<int:id>', views.trip_info),
    path('join/<int:id>',views.join)
]
