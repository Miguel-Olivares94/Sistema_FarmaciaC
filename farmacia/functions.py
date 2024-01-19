from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseServerError

def LogIn(request, username, password):
    try:
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            # Redirige al usuario a la página deseada después del inicio de sesión
            return redirect('farmacia_main')
        else:
            # Si la autenticación falla o el usuario no está activo, muestra un mensaje de error
            messages.error(request, 'Credenciales incorrectas o usuario inactivo.')
            # Puedes redirigir a la página de inicio de sesión o cualquier otra página
            return render(request, 'inicio_sesion.html')
    except Exception as e:
        # Maneja cualquier otra excepción que pueda ocurrir durante el proceso de inicio de sesión
        return HttpResponseServerError(f"Error durante el inicio de sesión: {str(e)}")
