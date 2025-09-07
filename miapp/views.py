# Vista para la página de contacto
from django.shortcuts import render

def contacto(request):
    return render(request, 'contacto.html')
from django.contrib.auth.decorators import login_required, user_passes_test
# Vista para el panel de admin con todos los números por hoja
@login_required
@user_passes_test(lambda u: u.is_superuser)
def panel_admin_numeros(request):
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
    premios_qs = Premio.objects.all()
    return render(request, "premios.html", {"premios": premios_qs})


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
    # Ordenar por categoría usando anotación para asegurar el orden en la base de datos
    from django.db.models import Case, When, IntegerField
    premios_qs = Premio.objects.annotate(
        categoria_orden=Case(
            When(categoria='1er', then=0),
            When(categoria='2do', then=1),
            When(categoria='3er', then=2),
            default=99,
            output_field=IntegerField(),
        )
    ).order_by('categoria_orden')
    return render(request, "premios.html", {"premios": premios_qs})

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

