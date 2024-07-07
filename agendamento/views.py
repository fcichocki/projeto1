
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Agendamento, Profissional
from .forms import AgendamentoForm
from datetime import time

HORARIOS_DISPONIVEIS = [
    time(8, 0),
    time(9, 0),
    time(10, 0)
]


def enviar_email(assunto, conteudo, destinatarios):
    email = EmailMessage(
        subject=assunto,
        body=conteudo,
        from_email='thebrazilianportuguesecourse@gmail.com',
        to=destinatarios,
    )
    email.send()


def agendar(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, user=request.user)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            agendamento.save()

            # Enviar email de confirmação
            assunto = "Confirmação de Agendamento"
            conteudo = f"Olá {agendamento.nome}, seu agendamento foi criado com sucesso para {
                agendamento.data.strftime('%d/%m/%Y')} às {agendamento.horario}."
            enviar_email(assunto, conteudo, [agendamento.email])

            messages.success(request, 'Agendamento cadastrado com sucesso.')
            return redirect('agendar')
    else:
        form = AgendamentoForm(user=request.user)
    return render(request, 'agendamento/agendar.html', {'form': form})


def agendar_adm(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user.username)
    return render(request, 'agendamento/agendar_adm.html', {'agendamentos': agendamentos})


def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso.')
        return redirect('agendar_adm')


def horarios_disponiveis(request):
    data = request.GET.get('data')
    profissional = request.GET.get('profissional')
    agendamentos = Agendamento.objects.filter(
        data=data, profissional=profissional)
    horarios_agendados = [agendamento.horario for agendamento in agendamentos]
    horarios_livres = [
        horario for horario in HORARIOS_DISPONIVEIS if horario not in horarios_agendados
    ]
    return JsonResponse(horarios_livres, safe=False)


# views.py


def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    if request.method == 'POST':
        form = AgendamentoForm(
            request.POST, instance=agendamento, user=request.user)
        if form.is_valid():
            agendamento = form.save(commit=False)
            profissional_id = request.POST.get('profissional')
            profissional = Profissional.objects.get(id=profissional_id)
            agendamento.profissional = profissional
            agendamento.save()
            messages.success(request, 'Agendamento editado com sucesso.')
            return redirect('agendar_adm')
    else:
        form = AgendamentoForm(instance=agendamento, user=request.user)
    return render(request, 'agendamento/editar_agendamento.html', {'form': form, 'agendamento': agendamento})


def horarios_disponiveis_edicao(request):
    if request.method == 'GET':
        data_str = request.GET.get('data')
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        agendamentos = Agendamento.objects.filter(data=data)
        horarios_agendados = [agendamento.horario.strftime(
            '%H:%M') for agendamento in agendamentos]
        horarios_disponiveis = [
            '08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'
        ]
        horarios_livres = [
            horario for horario in horarios_disponiveis if horario not in horarios_agendados
        ]
        response_data = {
            data_str: horarios_livres
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
