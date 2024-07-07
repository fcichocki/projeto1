from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Anotacao
from pacientes.models import Paciente


def ver_anotacoes(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    anotacao, created = Anotacao.objects.get_or_create(paciente=paciente)

    context = {
        'paciente': paciente,
        'anotacao': anotacao,
    }

    if 'ajax' in request.GET:
        return JsonResponse({'anotacao': anotacao.anotacoes})

    return render(request, 'detalhes_paciente.html', context)


@require_POST
def save_anotacoes(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    anotacao_texto = request.POST.get('anotacoes', '').strip()

    if anotacao_texto:  # Garante que não é vazio
        anotacao, created = Anotacao.objects.get_or_create(paciente=paciente)
        anotacao.anotacoes = anotacao_texto
        anotacao.save()
        return JsonResponse({"status": "success", "message": "Dados salvos com sucesso!"})
    else:
        return JsonResponse({"status": "error", "message": "Não foi possível salvar dados vazios."})
