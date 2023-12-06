from django.urls import path,include
from django.urls import path, include
from .views import CerrarSesionView
from .views import ventas,realizar_venta,eliminar_venta, actualizar_venta
from .views import detalle_venta
from .views import (

    FarmaciaMainView,
    MedicamentoListView,
    MedicamentoDetailView,
    MedicamentoCreateView,
    MedicamentoUpdateView,
    MedicamentoDeleteView,
    ProveedorListView,
    ProveedorDetailView,
    ProveedorCreateView,
    ProveedorUpdateView,
    ProveedorDeleteView,
    RegistroUsuarioView,
    InicioSesionView,
    
    
)



urlpatterns = [
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('farmacia_main/', FarmaciaMainView.as_view(), name='farmacia_main'),
    
    path('ventas/', ventas, name='ventas'),
    path('realizar_venta/', realizar_venta, name='realizar_venta'),
    path('ventas/eliminar/<int:venta_id>/', eliminar_venta, name='eliminar_venta'),
    path('ventas/actualizar/<int:venta_id>/', actualizar_venta, name='actualizar_venta'),
    path('venta/<int:venta_id>/', detalle_venta, name='detalle_venta'),
   

    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('', InicioSesionView.as_view(), name='inicio_sesion'),
    path('cerrar_sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),
    
    
    path('medicamentos/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/<int:pk>/', MedicamentoDetailView.as_view(), name='medicamento_detail'),
    path('medicamentos/nuevo/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/<int:pk>/editar/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamentos/<int:pk>/eliminar/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),
    
    
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('proveedores/nuevo/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
]

