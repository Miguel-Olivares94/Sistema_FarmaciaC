# farmacia/views.py

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
from django.db.models import F

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from .forms import VentaForm
from .models import Medicamento, Venta
from django.db.models import Sum, F
from django.db import models



# view medicametos
class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'farmacia/medicamento_list.html'
    context_object_name = 'medicamentos'


class FarmaciaMainView(View):
    template_name = 'farmacia/farmacia_main.html'

    def get(self, request):
        total_medicamentos = Medicamento.objects.count()
        medicamentos_agotados = Medicamento.objects.filter(stock=0).count()

        context = {
            'total_medicamentos': total_medicamentos,
            'medicamentos_agotados': medicamentos_agotados,
        }

        return render(request, self.template_name, context)

class MedicamentoListView(View):
    template_name = 'farmacia/medicamento_list.html'

    def get(self, request):
        medicamentos = Medicamento.objects.all()
        context = {'medicamentos': medicamentos}
        return render(request, self.template_name, context)

class MedicamentoDetailView(View):
    template_name = 'farmacia/medicamento_detail.html'

    def get(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        return render(request, self.template_name, {'medicamento': medicamento})

from django.shortcuts import render, reverse, HttpResponseRedirect

class MedicamentoCreateView(View):
    template_name = 'farmacia/medicamento_form.html'

    def get(self, request):
        form = MedicamentoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            print("Medicamento guardado con éxito")
            return HttpResponseRedirect(reverse('medicamento_list'))
        else:
            print("Formulario no válido. Errores:")
            print(form.errors)
        
        return render(request, self.template_name, {'form': form})


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

class MedicamentoDeleteView(View):
    template_name = 'farmacia/medicamento_confirm_delete.html'

    def get(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        return render(request, self.template_name, {'medicamento': medicamento})

    def post(self, request, pk):
        medicamento = get_object_or_404(Medicamento, pk=pk)
        medicamento.delete()
        return HttpResponseRedirect(reverse('medicamento_list'))

# Vistas para los proveedores

class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'farmacia/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'farmacia/proveedor_detail.html'
    context_object_name = 'proveedor'

class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'farmacia/proveedor_form.html'
    fields = ['nombre', 'razon_social', 'rut', 'direccion', 'email', 'fono', 'productos']
    def get_success_url(self):
        return reverse('proveedor_detail', args=[str(self.object.id)])

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = 'farmacia/proveedor_form.html'
    fields = ['nombre', 'razon_social', 'rut', 'direccion', 'email', 'fono', 'productos']

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'farmacia/proveedor_confirm_delete.html'
    success_url = reverse_lazy('proveedor_list')
    




def dashboard(request):
    # Obtener el stock de cada medicamento y calcular el nivel de stock actual
    medicamentos = Medicamento.objects.all()
    for medicamento in medicamentos:
        medicamento.nivel_stock = medicamento.get_nivel_stock()

    # Obtener el stock vendido sumando la cantidad de todas las ventas
    stock_vendido = Venta.objects.aggregate(total_stock_vendido=Sum('cantidad'))
    total_stock_vendido = stock_vendido['total_stock_vendido'] or 0  # Manejar el caso de que sea None

    # Obtener la cantidad total de ventas
    total_ventas = Venta.objects.count()

    # Obtener el monto total vendido sumando los precios de todas las ventas
    monto_total_vendido = Venta.objects.aggregate(total_monto_vendido=Sum('precio'))
    total_monto_vendido = monto_total_vendido['total_monto_vendido'] or 0  # Manejar el caso de que sea None

    return render(request, 'dashboard.html', {
        'medicamentos': medicamentos,
        'stock_vendido': total_stock_vendido,
        'total_ventas': total_ventas,
        'monto_total_vendido': total_monto_vendido,
    })

def realizar_venta(request):
    
    if request.method == 'POST':
        # Crea una instancia del formulario VentaForm con los datos de la solicitud
        form = VentaForm(request.POST)
        # Verifica si el formulario es válido
        if form.is_valid():
            # Guarda la venta en la base de datos sin realizar la commit aún
            venta = form.save(commit=False)
            # Asigna al vendedor el usuario que realizó la solicitud
            venta.vendedor = request.user
            # Guarda la venta en la base de datos
            venta.save()

            # Itera sobre los medicamentos seleccionados en el formulario
            for medicamento in form.cleaned_data['medicamentos']:
                # Obtiene la cantidad vendida específica para cada medicamento
                cantidad = form.cleaned_data['cantidad_medicamentos'][medicamento.pk]

                # Obtiene el objeto Medicamento desde la base de datos
                medicamento_obj = get_object_or_404(Medicamento, pk=medicamento.pk)

                # Verifica si hay suficiente stock para la venta
                if medicamento_obj.stock >= cantidad:
                    # Resta la cantidad vendida al stock en la base de datos usando F expressions
                    Medicamento.objects.filter(id=medicamento_obj.id).update(stock=F('stock') - cantidad)
                    # Actualiza el objeto actual con los valores de la base de datos
                    medicamento_obj.refresh_from_db()

                    # Crea el detalle de la venta
                    detalle_venta = Venta(medicamento=medicamento_obj, cantidad=cantidad, precio=venta.precio)
                    detalle_venta.save()

                    # Muestra un mensaje en la consola con información sobre la venta y el stock actualizado
                    print(f"Venta realizada para {medicamento_obj.nombre}. Stock actualizado: {medicamento_obj.stock}")
                else:
                    # Muestra un mensaje de error si no hay suficiente stock y redirige a la página correspondiente
                    messages.error(request, f"No hay suficiente stock para {medicamento_obj.nombre}")
                    return redirect('error_stock_insuficiente')

            # Muestra un mensaje de éxito y redirige a la página de ventas
            messages.success(request, "Venta realizada con éxito.")
            return redirect('ventas')
    else:
        # Si la solicitud no es un POST, crea una instancia del formulario VentaForm vacío
        form = VentaForm()

    # Renderiza la página 'realizar_venta.html' con el formulario
    return render(request, 'farmacia/realizar_venta.html', {'form': form})




def ventas(request):
    # Obtén todas las ventas
    ventas = Venta.objects.all()

    # Itera sobre las ventas y resta la cantidad al stock
    for venta in ventas:
        # Obtén el medicamento asociado a la venta
        medicamento = venta.medicamento

        # Resta la cantidad vendida al stock
        medicamento.stock -= venta.cantidad

        # Guarda los cambios en el stock
        medicamento.save()

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


class InicioSesionView(View):
    template_name = 'farmacia/inicio_sesion.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('farmacia_main')) 
        return render(request, self.template_name, {'form': form})
    
class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        return redirect('inicio_sesion')



  
