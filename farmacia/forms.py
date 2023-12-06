# farmacia/forms.py
from django import forms
from .models import Medicamento
from django.contrib.auth.forms import UserCreationForm
from .models import Venta

class VentaForm(forms.ModelForm):
    cantidad_medicamentos = forms.IntegerField(
        label='Cantidad de Medicamentos',
        required=True,
    )

    class Meta:
        model = Venta
        fields = '__all__'

    medicamentos = forms.ModelMultipleChoiceField(
        queryset=Medicamento.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Medicamentos'
    )


class Meta:
    model = Venta
    fields = '__all__'

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        
    medicamentos = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple, required=False)


class RegistrationForm(UserCreationForm):
    # Puedes agregar campos adicionales si es necesario
    email = forms.EmailField()
        
#medicamento

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel_stock'].required = False

    NIVEL_STOCK_CHOICES = [
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
    ]

    nivel_stock = forms.ChoiceField(
        choices=NIVEL_STOCK_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Nivel de Stock' 
    )


