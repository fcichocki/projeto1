from django.utils import timezone
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Agenda
from profissionais.models import Profissional
import smtplib
from email.message import EmailMessage
from django.utils.dateformat import DateFormat


# Salva agendamentos na página do usuário - apenas salva sem listar

def cadastrar_agenda(request):
    profissionais = Profissional.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')
        hora = request.POST.get('hora')
        profissional_id = request.POST.get('profissional')
        profissional = get_object_or_404(Profissional, id=profissional_id)

        data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()

        Agenda.objects.create(
            nome=nome, email=email, telefone=telefone, data=data_obj, hora=hora,
            profissional=profissional
        )

        assunto = "Confirmação de Agendamento"
        conteudo = f"Olá {nome}, seu agendamento foi criado com sucesso para {
            data_obj.strftime('%d/%m/%Y')} às {hora}."

        # Enviar email apenas para o paciente
        enviar_email(assunto, conteudo, [email])

        messages.success(request, 'Agendamento cadastrado com sucesso.')
        return redirect('cadastrar_agenda')

    return render(request, 'cadastrar_agenda.html', {
        'profissionais': profissionais,
        'horarios': horarios
    })


def listar_agendamentos(request):
    profissionais = Profissional.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]
    agendamentos = Agenda.objects.all().order_by('data', 'hora')
    agendamentos_do_dia = Agenda.objects.filter(
        data=timezone.now().date()).order_by('hora')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')
        hora = request.POST.get('hora')
        profissional_id = request.POST.get('profissional')
        profissional = Profissional.objects.get(id=profissional_id)

        data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()

        novo_agendamento = Agenda.objects.create(
            nome=nome, email=email, telefone=telefone, data=data_obj, hora=hora,
            profissional=profissional
        )

        data_formatada = data_obj.strftime('%d/%m/%Y')

        assunto = "Confirmação de Agendamento"
        conteudo = f"Olá {nome}, seu agendamento foi criado com sucesso para {
            data_formatada} às {hora}."
        enviar_email(assunto, conteudo, [email])

        messages.success(request, 'Agendamento cadastrado com sucesso.')

    return render(request, 'agendamentos.html', {
        'profissionais': profissionais,
        'horarios': horarios,
        'agendamentos': agendamentos,
        'agendamentos_do_dia': agendamentos_do_dia
    })


def excluir_agendamento(request, id_agendamento):
    agendamento = get_object_or_404(Agenda, id=id_agendamento)
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso.')
        return redirect('listar_agendamentos')
    return render(request, 'confirmar_exclusao.html', {'agendamento': agendamento})


def editar_agendamento(request, id_agendamento):
    agendamento = get_object_or_404(Agenda, id=id_agendamento)
    profissionais = Profissional.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]

    if request.method == 'POST':
        agendamento.nome = request.POST.get('nome')
        agendamento.email = request.POST.get('email')
        agendamento.telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')  # Recebendo a data como string
        agendamento.hora = request.POST.get('hora')
        agendamento.profissional_id = request.POST.get('profissional')

        # Convertendo a string de data para um objeto de data
        data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()
        agendamento.data = data_obj

        agendamento.save()

        # Formatando a data para o padrão dd/MM/yyyy
        data_formatada = data_obj.strftime('%d/%m/%Y')

        assunto = "Agendamento Atualizado"
        conteudo = f"Olá {agendamento.nome}, seu agendamento foi atualizado para {
            data_formatada} às {agendamento.hora}."
        enviar_email(assunto, conteudo, [agendamento.email])

        messages.success(request, 'Agendamento atualizado com sucesso.')
        return redirect('listar_agendamentos')

    return render(request, 'editar_agendamento.html', {
        'agendamento': agendamento,
        'profissionais': profissionais,
        'horarios': horarios
    })


def enviar_email(assunto, conteudo, destinatarios):
    EMAIL_ADDRESS = "thebrazilianportuguesecourse@gmail.com"
    EMAIL_PASSWORD = "afgd uzzq muwk kiua"

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(destinatarios)
    msg.set_content(conteudo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
