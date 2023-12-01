from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

# Create your views here.
class tipoUsuarioView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            tipos=list(tipoUsuario.objects.filter(id=id).values())
            if len(tipos) > 0:
                tipo = tipos[0]
                datos = {'message':'Success', 'tipos':tipo}
            else:
                datos = {'message':'tipo no encontrado'}
            return JsonResponse(datos)
        else:
            tipos = list(tipoUsuario.objects.values())
            if len(tipos) > 0:
                datos = {'message':'Success', 'tipos':tipos}
            else:
                datos = {'message':'tipos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        tipoUsuario.objects.create(tipo=jd['tipo'])
        datos = {'message':'Success'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        tipos=list(tipoUsuario.objects.filter(id=id).values())
        if len(tipos) > 0:
            tipo = tipoUsuario.objects.get(id=id)
            tipo.tipo = jd['tipo']
            tipo.save()
            datos = {'message':'Success'}
        else:
            datos = {'message':'tipo no encontrado'}
        return JsonResponse(datos)

    def delete(self, request, id):
        tipos=list(tipoUsuario.objects.filter(id=id).values())
        if len(tipos) > 0:
            tipoUsuario.objects.filter(id=id).delete()
            datos = {'message':'Success'}
        else:
            datos = {'message':'tipo no encontrado'}
        return JsonResponse(datos)
        
