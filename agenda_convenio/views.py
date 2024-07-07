
from email.message import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AgendaConvenio
from profissionais.models import Profissional
from convenios.models import Convenio
import datetime
import smtplib

# FUNÇÃO CADASTRAR DA TELA EXIBIDA AO CLIENTE


def cadastrar_agenda_convenio(request):
    profissionais = Profissional.objects.all()
    convenios = Convenio.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')
        hora = request.POST.get('hora')
        profissional_id = request.POST.get('profissional')
        convenio_id = request.POST.get('convenio')

        profissional = Profissional.objects.get(id=profissional_id)
        convenio = Convenio.objects.get(id=convenio_id)
        data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()

        AgendaConvenio.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            data=data_obj,
            hora=hora,
            profissional=profissional,
            convenio=convenio
        )

        data_formatada = data_obj.strftime('%d/%m/%Y')
        assunto = "Confirmação de Agendamento"
        conteudo = f"Prezado(a) {nome}, seu agendamento foi realizado com sucesso para {
            data_formatada} às {hora}."
        enviar_email(assunto, conteudo, email)

        messages.success(
            request, "Agendamento realizado com sucesso, você receberá um email com maiores informações.")
        return redirect('cadastrar_agenda_convenio')

    return render(request, 'cadastrar_agenda_convenio.html', {
        'profissionais': profissionais,
        'convenios': convenios,
        'horarios': horarios
    })

# FUNÇÃO DA TELA EXIBIDA AO ADMINISTRADOR, CADASTRA E LISTA AGENDAMENTOS


def listar_e_cadastrar_agendamentos_convenio(request):
    profissionais = Profissional.objects.all()
    convenios = Convenio.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]
    agendamentos = AgendaConvenio.objects.all().order_by('data', 'hora')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')
        hora = request.POST.get('hora')
        profissional_id = request.POST.get('profissional')
        convenio_id = request.POST.get('convenio')

        profissional = Profissional.objects.get(id=profissional_id)
        convenio = Convenio.objects.get(id=convenio_id)
        data_obj = datetime.datetime.strptime(data_str, '%Y-%m-%d').date()

        AgendaConvenio.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            data=data_obj,
            hora=hora,
            profissional=profissional,
            convenio=convenio
        )

        data_formatada = data_obj.strftime('%d/%m/%Y')
        assunto = "Confirmação de Agendamento"
        conteudo = f"Prezado(a) {nome}, seu agendamento foi realizado com sucesso para {
            data_formatada} às {hora}."
        enviar_email(assunto, conteudo, email)

        return redirect('listar_e_cadastrar_agendamentos_convenio')

    return render(request, 'agendamentos-convenio.html', {
        'profissionais': profissionais,
        'convenios': convenios,
        'horarios': horarios,
        'agendamentos': agendamentos
    })


def excluir_agendamento_convenio(request, id):
    if request.method == 'POST':
        agendamento = get_object_or_404(AgendaConvenio, id=id)
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso.')
        return redirect('listar_e_cadastrar_agendamentos_convenio')


def editar_agendamento_convenio(request, id):
    agendamento = get_object_or_404(AgendaConvenio, id=id)
    profissionais = Profissional.objects.all()
    convenios = Convenio.objects.all()
    horarios = ["09:00", "10:00", "11:00", "13:00",
                "14:00", "15:00", "16:00", "17:00"]

    if request.method == 'POST':
        agendamento.nome = request.POST.get('nome')
        agendamento.email = request.POST.get('email')
        agendamento.telefone = request.POST.get('telefone')
        data_str = request.POST.get('data')
        agendamento.hora = request.POST.get('hora')
        agendamento.profissional_id = request.POST.get('profissional')
        agendamento.convenio_id = request.POST.get('convenio')

        agendamento.data = datetime.datetime.strptime(
            data_str, '%Y-%m-%d').date()

        agendamento.save()

        data_formatada = agendamento.data.strftime('%d/%m/%Y')
        assunto = "Atualização de Agendamento"
        conteudo = f"Prezado(a) {agendamento.nome}, seu agendamento foi atualizado com sucesso para {
            data_formatada} às {agendamento.hora}."
        enviar_email(assunto, conteudo, agendamento.email)

        messages.success(request, 'Agendamento atualizado com sucesso.')
        return redirect('listar_e_cadastrar_agendamentos_convenio')

    return render(request, 'editar_agendamento_convenio.html', {
        'agendamento': agendamento,
        'profissionais': profissionais,
        'convenios': convenios,
        'horarios': horarios
    })


def enviar_email(assunto, conteudo, destinatarios):
    EMAIL_ADRESS = "thebrazilianportuguesecourse@gmail.com"
    EMAIL_PASSWORD = "afgd uzzq muwk kiua"

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADRESS
    msg['To'] = destinatarios
    msg.set_content(conteudo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
