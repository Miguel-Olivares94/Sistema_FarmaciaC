# farmacia/forms.py
from django import forms
from .models import Medicamento
from django.contrib.auth.forms import UserCreationForm
from .models import Venta
from django.contrib.auth.forms import AuthenticationForm

class CaseInsensitiveAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form to make the username case-insensitive.
    """

    def clean_username(self):
        return self.cleaned_data['username'].lower()


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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    numero_celular = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'numero_celular')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

        
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


