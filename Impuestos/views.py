#Librerías
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
import calendar

#Modelos
from Ventas.models import Factura
from Configuracion.models import Costos






def index(request):
    try:
        # Verifica si el usuario tiene el permiso necesario
        if not request.user.has_perm('Impuestos.view_parametros'):
            raise PermissionDenied

        return render(request, 'indexinitialTaxes.html')
    
    except PermissionDenied:
        messages.error(request, 'No tienes permiso para ver esta página.')
        # Obtener la URL anterior o redirigir a 'home' si no hay URL previa
        previous_url = request.META.get('HTTP_REFERER', 'home')
        return redirect(previous_url)





# TODO Make index template with all the information
def indexTaxes(request):
    if request.method == 'POST':
        bimestre = int(request.POST.get('bimestre', 0))  # Obtener el bimestre del formulario

        # Obtener el rango bimensual basado en el bimestre
        inicio_rango, fin_rango = get_bimonthly_range(bimestre)

        # Calcular las ventas y otros valores para el rango seleccionado
        ingresosBrutos = calculateSales(inicio_rango, fin_rango)
        IBC = calculateIBC(ingresosBrutos)
        costos = calculateCostos(inicio_rango, fin_rango)

        ingresosDepurados = ingresosBrutos - costos

        salud = calculateSalud(IBC)
        pension = calculatePension(IBC)
        cajaDeCompensacion = calculateCaja(IBC)
        ARL = 0 
        INCRNGO = calculateINCRNGO(inicio_rango, fin_rango)

        aportes = salud + pension + cajaDeCompensacion

        return render(request, 'indexTaxes.html', {
            'sales': ingresosBrutos, 'costos': costos,
            'IBC': IBC,
            'aportes': aportes,
            'salud': salud, 
            'pension': pension, 
            'cajaDeCompensacion': cajaDeCompensacion, 
            'ARL': ARL, 
            'ingresosDepurados': ingresosDepurados,
            'INCRNGO': INCRNGO 
        })
    else:
        # Manejo de método GET si es necesario
        return render(request, 'indexinitialTaxes.html')




def get_bimonthly_range(bimestre):
    año_actual = timezone.now().year
    
    # Definir los rangos bimensuales
    if bimestre == 1:
        inicio_rango = datetime(año_actual, 1, 1)
        fin_rango = datetime(año_actual, 2, calendar.monthrange(año_actual, 2)[1], 23, 59, 59)
    elif bimestre == 2:
        inicio_rango = datetime(año_actual, 3, 1)
        fin_rango = datetime(año_actual, 4, 30, 23, 59, 59)
    elif bimestre == 3:
        inicio_rango = datetime(año_actual, 5, 1)
        fin_rango = datetime(año_actual, 6, 30, 23, 59, 59)
    elif bimestre == 4:
        inicio_rango = datetime(año_actual, 7, 1)
        fin_rango = datetime(año_actual, 8, 31, 23, 59, 59)
    elif bimestre == 5:
        inicio_rango = datetime(año_actual, 9, 1)
        fin_rango = datetime(año_actual, 10, 31, 23, 59, 59)
    elif bimestre == 6:
        inicio_rango = datetime(año_actual, 11, 1)
        fin_rango = datetime(año_actual, 12, 31, 23, 59, 59)
    else:
        raise ValueError("Bimestre inválido")

    return inicio_rango, fin_rango






def calculateSales(inicio_rango, fin_rango):
    # Filtrar facturas dentro del rango
    ventas = Factura.objects.filter(
        fecha__range=[inicio_rango, fin_rango]
    ).aggregate(sales=Sum('total_con_iva'))
    
    return ventas['sales'] if ventas['sales'] else 0
 




def calculateIBC(ingresosBrutos):

    return ingresosBrutos/100*40 #Formula para el IBC





# TODO Calculate heath
def calculateSalud(IBC):
    salud = float(IBC) / 100 * 8.5
    return salud






# TODO Calculate pesión
def calculatePension(IBC):
    pension = float(IBC) / 100 * 12
    return pension





# TODO Calculate caja de compensación familiar
def calculateCaja(IBC):
    caja = float(IBC) / 100 * 4
    return caja





# TODO Calculate nomine
def calculateNomine():
    
    nomine = 0

    return nomine 





def calculateCostos(inicio_rango, fin_rango):
    costos = Costos.objects.filter(
        fecha__range=[inicio_rango, fin_rango]
    ).exclude(tipo_id=4).aggregate(valorcitos=Sum('valor'))
    
    return costos['valorcitos'] if costos['valorcitos'] else 0





def calculateINCRNGO(inicio_rango, fin_rango):
    costos = Costos.objects.filter(
        fecha__range=[inicio_rango, fin_rango],
        tipo_id=4
    ).aggregate(valorcitos=Sum('valor'))
    
    return costos['valorcitos'] if costos['valorcitos'] else 0





def calculateICA():
    
    
    
    return 0    





# TODO Calculate taxes
def calculateTaxes():
    
    taxes = 0

    return taxes