from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexClientes, name='indexClientes'),
    path('crearCliente/', views.crearCliente, name='crearCliente'),
    path('editar/<int:clienteID>/', views.editCliente, name='editCliente'),
    path('eliminar/<int:clienteID>/', views.eliminarCliente, name='eliminarCliente'),

]