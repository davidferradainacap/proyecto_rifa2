
# --- IMPORTS ---
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Numero, Premio, Publicidad
from .forms import PremioForm, PublicidadForm
from django.views.decorators.http import require_POST

# --- BORRAR PREMIOS SECUNDARIOS ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def borrar_premios_secundarios(request):
    Premio.objects.filter(categoria='sec').delete()
    return redirect('gestor_premios')

# --- BORRAR TODOS LOS PREMIOS ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def borrar_todos_premios(request):
    Premio.objects.all().delete()
    return redirect('premios')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def gestor_publicidad(request):
    publicidades = Publicidad.objects.order_by('-creado')
    if request.method == 'POST':
        form = PublicidadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestor_publicidad')
    else:
        form = PublicidadForm()
    return render(request, 'gestor_publicidad.html', {'publicidades': publicidades, 'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def borrar_publicidad(request, pk):
    publicidad = get_object_or_404(Publicidad, pk=pk)
    publicidad.delete()
    return redirect('gestor_publicidad')

# --- GESTOR DE PREMIOS ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
def gestor_premios(request):
    # Agrupar premios por categoría y ordenar por nombre
    categorias = [
        ('1er', '1er Lugar'),
        ('2do', '2do Lugar'),
        ('3er', '3er Lugar'),
        ('sec', 'Secundario'),
    ]
    premios_por_categoria = []
    for cat_key, cat_label in categorias:
        premios_cat = Premio.objects.filter(categoria=cat_key).order_by('nombre')
        premios_por_categoria.append((cat_label, premios_cat))
    if request.method == 'POST':
        form = PremioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestor_premios')
    else:
        form = PremioForm()
    return render(request, 'gestor_premios.html', {'premios_por_categoria': premios_por_categoria, 'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_premio(request, pk):
    premio = Premio.objects.get(pk=pk)
    if request.method == 'POST':
        form = PremioForm(request.POST, request.FILES, instance=premio)
        if form.is_valid():
            form.save()
            return redirect('gestor_premios')
    else:
        form = PremioForm(instance=premio)
    return render(request, 'gestor_premios.html', {'premios': Premio.objects.all(), 'form': form, 'editar': True, 'premio_editar': premio})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def borrar_premio(request, pk):
    premio = Premio.objects.get(pk=pk)
    if request.method == 'POST':
        premio.delete()
        return redirect('gestor_premios')

# Vista para mostrar todos los números por hoja solo para admin
@login_required
@user_passes_test(lambda u: u.is_superuser)
def detalle_numeros_admin(request):
    hoja = int(request.GET.get('hoja', 1))
    hojas = [1, 2, 3, 4]
    numeros = Numero.objects.filter(hoja=hoja).order_by('valor')
    return render(request, "detalle_numeros_admin.html", {"numeros": numeros, "hoja": hoja, "hojas": hojas})

# Vista para que el admin vea todos los números con información
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_todos_numeros(request):
    numeros = Numero.objects.all().order_by('hoja', 'valor')
    return render(request, "admin_todos_numeros.html", {"numeros": numeros})

# Vista para la página de contacto
def contacto(request):
    return render(request, 'contacto.html')

# Vista para el panel de admin con todos los números por hoja
@login_required
@user_passes_test(lambda u: u.is_superuser)
def panel_admin_numeros(request):
    if request.method == 'POST':
        # Procesar todos los números de la hoja
        ids = [k.split('_')[1] for k in request.POST.keys() if k.startswith('numero_id_')]
        for numero_id in ids:
            numero = get_object_or_404(Numero, id=numero_id)
            numero.gmail = request.POST.get(f'gmail_{numero_id}', '')
            numero.nombre_completo = request.POST.get(f'nombre_completo_{numero_id}', '')
            numero.telefono = request.POST.get(f'telefono_{numero_id}', '')
            numero.disponible = f'disponible_{numero_id}' in request.POST
            numero.asistencia = f'asistencia_{numero_id}' in request.POST
            numero.save()
        return redirect('admin_numeros')
    hojas = []
    for h in range(1, 5):
        nums = Numero.objects.filter(hoja=h).order_by('valor')
        hojas.append({'hoja': h, 'numeros': nums})
    return render(request, "panel_admin_numeros.html", {"hojas": hojas})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Numero, Premio, EstadoRuleta
import random

DURACION_RULETA = 10.0  # segundos

def home(request):
    return render(request, "home.html")


# Hoja 1: Números hoja=1
def numeros(request):
    nums = Numero.objects.filter(hoja=1).order_by('valor')
    return render(request, "numeros.html", {"numeros": nums, "hoja": 1})

# Hoja 2: Números hoja=2
def numeros_hoja2(request):
    nums = Numero.objects.filter(hoja=2).order_by('valor')
    return render(request, "numeros.html", {"numeros": nums, "hoja": 2})

# Hoja 3: Números hoja=3
def numeros_hoja3(request):
    nums = Numero.objects.filter(hoja=3).order_by('valor')
    return render(request, "numeros.html", {"numeros": nums, "hoja": 3})

# Hoja 4: Números hoja=4
def numeros_hoja4(request):
    nums = Numero.objects.filter(hoja=4).order_by('valor')
    return render(request, "numeros.html", {"numeros": nums, "hoja": 4})

def admin_numeros(request):
    nums = Numero.objects.all()
    return render(request, "admin_numeros.html", {"numeros": nums})

def premios(request):
    premios_qs = Premio.objects.exclude(categoria='sec')
    premios_secundarios = Premio.objects.filter(categoria='sec')
    publicidades = Publicidad.objects.order_by('-creado')
    return render(request, "premios.html", {
        "premios": premios_qs,
        "publicidades": publicidades,
        "premios_secundarios": premios_secundarios
    })

def numero_detalle(request, pk):
    numero = get_object_or_404(Numero, pk=pk)
    return render(request, "numero_detalle.html", {"numero": numero})

@csrf_exempt
def iniciar_ruleta(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método inválido"})
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"ok": False, "error": "No autorizado"})
    vendidos = list(Numero.objects.filter(disponible=False).values_list('valor', flat=True))
    if not vendidos:
        return JsonResponse({"ok": False, "error": "No hay números vendidos"})
    EstadoRuleta.objects.all().delete()
    ganador = str(random.choice(vendidos))
    estado = EstadoRuleta.objects.create(
        en_progreso=True,
        inicio=timezone.now(),
        ganador=ganador
    )
    estado.set_numeros(vendidos)
    estado.save()
    return JsonResponse({"ok": True})

def estado_ruleta(request):
    estado = EstadoRuleta.objects.first()
    if not estado:
        return JsonResponse({"status": "idle"})
    ahora = timezone.now()
    elapsed = (ahora - estado.inicio).total_seconds() if estado.inicio else 0
    if estado.en_progreso and elapsed >= DURACION_RULETA:
        estado.en_progreso = False
        estado.save(update_fields=["en_progreso"])
    return JsonResponse({
        "status": "running" if estado.en_progreso else "finished",
        "inicio": estado.inicio.timestamp(),
        "duracion": DURACION_RULETA,
        "numeros": estado.get_numeros(),
        "ganador": None if estado.en_progreso else estado.ganador
    })

