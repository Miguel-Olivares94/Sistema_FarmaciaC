# farmacia/views.py
from .forms import CaseInsensitiveAuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Medicamento, Proveedor, Venta, DetalleVenta
from .forms import MedicamentoForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import VentaForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db import models
from django.db import transaction
from django.db.models import F



############################################ VISTAS ###############################################################################


######   Se define una clase basada en View para manejar el registro de usuarios ####


class RegistroUsuarioView(View):
    
    # Se especifica la plantilla que se utilizará para renderizar la página de registro
    template_name = 'farmacia/registro_usuario.html'

    # Método para manejar las solicitudes GET (al cargar la página)
    def get(self, request):
        # Crear una instancia del formulario de creación de usuarios
        form = UserCreationForm()
        # Renderizar la página de registro con el formulario
        return render(request, self.template_name, {'form': form})

    # Método para manejar las solicitudes POST (al enviar el formulario)
    def post(self, request):
        # Crear una instancia del formulario de creación de usuarios con los datos del POST
        form = UserCreationForm(request.POST)
        
        # Verificar si el formulario es válido
        if form.is_valid():
            # Guardar el usuario en la base de datos
            user = form.save()
            # Obtener el nombre de usuario y contraseña limpios del formulario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Autenticar al usuario recién creado
            user = authenticate(username=username, password=password)

            # Verificar si la autenticación fue exitosa
            if user is not None:
                # Iniciar sesión para el usuario autenticado
                login(request, user)
                # Mostrar un mensaje de éxito
                messages.success(request, '¡Registro exitoso!')
                # Redirigir al usuario a una URL específica (en este caso, 'farmacia_main')
                return redirect(reverse_lazy('farmacia_main'))
            else:
                # Si la autenticación falla, mostrar un mensaje de error
                messages.error(request, 'Error en el registro. Por favor, inténtalo de nuevo.')

        # Si el formulario no es válido, volver a renderizar el formulario con errores
        return render(request, self.template_name, {'form': form})
    
    
    


########### Se define una clase basada en View para manejar la vista de inicio de sesión##########

class InicioSesionView(View):
    template_name = 'farmacia/inicio_sesion.html'
    authentication_form = CaseInsensitiveAuthenticationForm

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Aquí es donde usamos tu formulario de registro con el campo de email
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('farmacia_main'))

        return render(request, self.template_name, {'form': form})
    
    
    
############## Se define una clase basada en View para manejar la vista de cierre de sesión ############################

class CerrarSesionView(View):
    
    # Método para manejar las solicitudes GET (al cargar la página)
    def get(self, request):
        # Cerrar la sesión del usuario actual
        logout(request)
        # Redirigir al usuario a la página de inicio de sesión ('inicio_sesion')
        return redirect('inicio_sesion')





# vista del menú principal de la farmacia 



############# Se define una clase basada en View para manejar la vista principal de la farmacia ########

class FarmaciaMainView(View):
    # Se especifica la plantilla que se utilizará para renderizar la página principal
    template_name = 'farmacia/farmacia_main.html'

    # Método para manejar las solicitudes GET (al cargar la página)
    def get(self, request):
        # Obtener el total de medicamentos en la base de datos
        total_medicamentos = Medicamento.objects.count()
        # Obtener la cantidad de medicamentos con stock agotado
        medicamentos_agotados = Medicamento.objects.filter(stock=0).count()

        # Crear un diccionario de contexto con la información obtenida
        context = {
            'total_medicamentos': total_medicamentos,
            'medicamentos_agotados': medicamentos_agotados,
        }

        # Renderizar la página principal con el contexto proporcionado
        return render(request, self.template_name, context)



####################################### Vistas de medicametos #################################################




###### Vista de inventario medicamento ######


########### Se define una clase basada en View para manejar la vista de lista de medicamentos #############
class MedicamentoListView(View):
    # Se especifica la plantilla que se utilizará para renderizar la lista de medicamentos
    template_name = 'farmacia/medicamento_list.html'

    # Método para manejar las solicitudes GET (al cargar la página)
    def get(self, request):
        
        # Obtener todos los medicamentos de la base de datos
        medicamentos = Medicamento.objects.all()
        
        # Crear un diccionario de contexto con la lista de medicamentos
        context = {'medicamentos': medicamentos}
        
        # Renderizar la página de lista de medicamentos con el contexto proporcionado
        return render(request, self.template_name, context)




###### Vista de Detalles de medicamento ######


class MedicamentoDetailView(View):
    template_name = 'farmacia/medicamento_detail.html'

    def get(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        return render(request, self.template_name, {'medicamento': medicamento})
    
    


###### Vista de Detalles de medicamento ###### 



############### Se define una clase basada en View para manejar la vista de creación de medicamentos###############

class MedicamentoCreateView(View):
    
    # Se especifica la plantilla que se utilizará para renderizar el formulario de creación
    template_name = 'farmacia/medicamento_form.html'

    # Método para manejar las solicitudes GET (al cargar la página)
    def get(self, request):
        # Crear una instancia del formulario de creación de medicamentos
        form = MedicamentoForm()
        # Renderizar la página de creación de medicamentos con el formulario vacío
        return render(request, self.template_name, {'form': form})

    # Método para manejar las solicitudes POST (al enviar el formulario)
    def post(self, request):
        # Crear una instancia del formulario de creación de medicamentos con los datos del POST
        form = MedicamentoForm(request.POST)
        
        # Verificar si el formulario es válido
        if form.is_valid():
            # Guardar el nuevo medicamento en la base de datos
            form.save()
            print("Medicamento guardado con éxito")
            # Redirigir a la lista de medicamentos
            return HttpResponseRedirect(reverse('medicamento_list'))
        else:
            # Si el formulario no es válido, imprimir errores en la consola
            print("Formulario no válido. Errores:")
            print(form.errors)
        
        # Si el formulario no es válido, volver a renderizar la página con errores
        return render(request, self.template_name, {'form': form})

    
    


###### Vista para Actualizar medicamento ###### 


class MedicamentoUpdateView(View):
    template_name = 'farmacia/medicamento_form.html'

    def get(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        form = MedicamentoForm(instance=medicamento)
        return render(request, self.template_name, {'form': form, 'medicamento': medicamento})

    def post(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('medicamento_list'))
        return render(request, self.template_name, {'form': form, 'medicamento': medicamento})
    
    
    

###### Vista para Eliminar medicamento ###### 


class MedicamentoDeleteView(View):
    template_name = 'farmacia/medicamento_confirm_delete.html'

    def get(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        return render(request, self.template_name, {'medicamento': medicamento})

    def post(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        medicamento.delete()
        return HttpResponseRedirect(reverse('medicamento_list'))
    
    
    
    
    
    

####################################### Vistas de medicametos #################################################



###### Vista del inventario de proveedores ###### 



class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'farmacia/proveedor_list.html'
    context_object_name = 'proveedores'


###### Vista del Detalle de Proveedor ###### 


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'farmacia/proveedor_detail.html'
    context_object_name = 'proveedor'



###### Vista para crear/guardar el proveedor ###### 


class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'farmacia/proveedor_form.html'
    fields = ['nombre', 'razon_social', 'rut', 'direccion', 'email', 'fono', 'productos']
    def get_success_url(self):
        return reverse('proveedor_detail', args=[str(self.object.id)])
    

###### Vista para actualizar de proveedor ###### 

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = 'farmacia/proveedor_form.html'
    fields = ['nombre', 'razon_social', 'rut', 'direccion', 'email', 'fono', 'productos']
    
###### Vista para eliminar el proveedor ###### 

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'farmacia/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')
    


####################################### Vistas de Dashboard #################################################
    


from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear
from .models import Medicamento, Venta

def dashboard(request):
    medicamentos = Medicamento.objects.all()

    # Obtener nivel de stock para cada medicamento
    for medicamento in medicamentos:
        medicamento.nivel_stock = medicamento.get_nivel_stock()

    total_stock_vendido = Venta.objects.aggregate(total_stock_vendido=Sum('cantidad'))['total_stock_vendido'] or 0

    total_ventas = Venta.objects.count()

    total_monto_vendido = Venta.objects.aggregate(total_monto_vendido=Sum('precio'))['total_monto_vendido'] or 0

    medicamentos_vendidos = [venta.medicamento.nombre for venta in Venta.objects.select_related('medicamento')]

    # Obtener estadísticas de ventas semanales, mensuales y anuales
    ventas_semanales = Venta.objects.annotate(week=TruncWeek('fecha')).values('week').annotate(total=Sum('precio')).order_by('week')
    ventas_mensuales = Venta.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(total=Sum('precio')).order_by('month')
    ventas_anuales = Venta.objects.annotate(year=TruncYear('fecha')).values('year').annotate(total=Sum('precio')).order_by('year')

    return render(request, 'dashboard.html', {
        'medicamentos': medicamentos,
        'stock_vendido': total_stock_vendido,
        'total_ventas': total_ventas,
        'monto_total_vendido': total_monto_vendido,
        'medicamentos_vendidos': medicamentos_vendidos,
        'ventas_semanales': ventas_semanales,
        'ventas_mensuales': ventas_mensuales,
        'ventas_anuales': ventas_anuales,
    })



   ############# Vista para realizar venta ############




def realizar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.vendedor = request.user
            venta.save()

            for medicamento in form.cleaned_data['medicamentos']:
                cantidad = form.cleaned_data['cantidad_medicamentos'][medicamento.pk]
                medicamento_obj = get_object_or_404(Medicamento, pk=medicamento.pk)

                if medicamento_obj.stock >= cantidad:
                    Medicamento.objects.filter(id=medicamento_obj.id).update(stock=F('stock') - cantidad)
                    medicamento_obj.refresh_from_db()

                    detalle_venta = Venta(medicamento=medicamento_obj, cantidad=cantidad, precio=venta.precio)
                    detalle_venta.save()

                    print(f"Venta realizada para {medicamento_obj.nombre}. Stock actualizado: {medicamento_obj.stock}")
                else:
                    messages.error(request, f"No hay suficiente stock para {medicamento_obj.nombre}")
                    return redirect('error_stock_insuficiente')

            messages.success(request, "Venta realizada con éxito.")
            return redirect('detalle_venta', venta_id=venta.id)
    else:
        form = VentaForm()

    return render(request, 'farmacia/realizar_venta.html', {'form': form})




def ventas(request):
    # Obtén todas las ventas
    ventas = Venta.objects.all()
    return render(request, 'farmacia/ventas.html', {'ventas': ventas})


def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    
    if request.method == 'POST':
        venta.delete()
        return redirect('ventas')

    return render(request, 'farmacia/eliminar_venta.html', {'venta': venta})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)

    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ventas')
    else:
        form = VentaForm(instance=venta)

    return render(request, 'farmacia/actualizar_venta.html', {'form': form, 'venta': venta})

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    detalle_venta = venta.detalleventa_set.first()  

    return render(request, 'farmacia/detalle_venta.html', {'venta': venta, 'detalle_venta': detalle_venta})

class RegistroUsuarioView(View):
    template_name = 'farmacia/registro_usuario.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '¡Registro exitoso!')
                return redirect(reverse_lazy('farmacia_main'))  
            else:
                messages.error(request, 'Error en el registro. Por favor, inténtalo de nuevo.')

        # Si el formulario no es válido, vuelve a renderizar el formulario con errores
        return render(request, self.template_name, {'form': form})





  
