from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from .models import Nota
from .forms import NotaForm, RegistroForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm




def get_query(request):
    """Función auxiliar para obtener query de búsqueda"""
    return request.GET.get('q', '')


@login_required
def lista_notas(request):
    # Obtener el término de búsqueda de la URL
    query = request.GET.get('q', '')
    
    # Filtrar notas del usuario actual
    notas = Nota.objects.filter(usuario=request.user)
    
    # Si hay término de búsqueda, filtrar por título
    if query:
        notas = notas.filter(titulo__icontains=query)
    
    return render(request, 'notas/lista_notas.html', {'notas': notas, 'query': query})

@login_required
def crear_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user  
            nota.save()
            messages.success(request, '¡Nota creada exitosamente!')
            return redirect('lista_notas')
    else:
        form = NotaForm()
    
    return render(request, 'notas/crear_nota.html', {'form': form})

@login_required
def editar_nota(request, nota_id):
    # Asegurar que solo se pueda editar notas del usuario
    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)
    
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Nota actualizada exitosamente!')
            return redirect('lista_notas')
    else:
        form = NotaForm(instance=nota)
    
    return render(request, 'notas/editar_nota.html', {'form': form, 'nota': nota})

@require_POST
@login_required
def eliminar_nota(request, nota_id):
    # Asegurar que solo se pueda eliminar notas del usuario
    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)
    nota.delete()
    messages.success(request, '¡Nota eliminada exitosamente!')
    return redirect('lista_notas')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('lista_notas')
    else:
        form = RegistroForm()
    
    return render(request, 'notas/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('lista_notas')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'notas/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

@login_required
def perfil(request):
    query = get_query(request)
    usuario = request.user
    
    # Asegurar que el usuario tiene perfil
    if not hasattr(usuario, 'perfil'):
        from .models import Perfil
        Perfil.objects.create(usuario=usuario)
    
    notas_count = Nota.objects.filter(usuario=usuario).count()
    
    if request.method == 'POST':
        # Actualizar perfil
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        
        # Validar teléfono (solo números, opcional)
        if telefono and not telefono.isdigit():
            messages.error(request, '❌ El teléfono solo debe contener números.')
            return redirect('perfil')
        
        if username:
            usuario.username = username
        if email:
            usuario.email = email
        
        usuario.save()
        
        # Actualizar teléfono en el perfil
        if telefono is not None:
            usuario.perfil.telefono = telefono if telefono else None
            usuario.perfil.save()
        
        messages.success(request, '✅ ¡Perfil actualizado exitosamente!')
        return redirect('perfil')
    
    return render(request, 'notas/perfil.html', {
        'usuario': usuario,
        'notas_count': notas_count,
        'query': query
    })

@login_required
def cambiar_password(request):
    query = get_query(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '✅ ¡Contraseña actualizada exitosamente!')
            return redirect('perfil')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'notas/reset_password.html', {
        'form': form,
        'query': query
    })