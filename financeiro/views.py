from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Despesa, Receita
from datetime import date
from pacientes.models import Paciente
from produtos.models import Produto
from decimal import Decimal


def cadastrar_receita(request):
    pacientes = Paciente.objects.filter(usuario=request.user.username)
    produtos = Produto.objects.filter(usuario=request.user.username)
    receitas = Receita.objects.filter(usuario=request.user).order_by('data')
    hoje = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        produto_id = request.POST.get('descricao')
        valor = request.POST.get('valor').replace(',', '.')
        data = request.POST.get('data')
        status = request.POST.get('status')
        forma_pagamento = request.POST.get('forma_pagamento')

        cliente = Paciente.objects.get(id=cliente_id)
        descricao = Produto.objects.get(id=produto_id)

        Receita.objects.create(
            cliente=cliente,
            descricao=descricao,
            valor=valor,
            data=data,
            status=status,
            forma_pagamento=forma_pagamento,
            usuario=request.user
        )

        return redirect('cadastrar_receita')

    return render(request, 'cadastrar_receita.html', {
        'pacientes': pacientes,
        'produtos': produtos,
        'receitas': receitas,
        'hoje': hoje,
    })


def excluir_receita(request, receita_id):
    if request.method == 'POST':
        receita = get_object_or_404(Receita, id=receita_id)
        receita.delete()
        return redirect('cadastrar_receita')
    return redirect('cadastrar_receita')


def editar_receita(request, receita_id):
    receita = get_object_or_404(Receita, id=receita_id)
    pacientes = Paciente.objects.all()
    produtos = Produto.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        produto_id = request.POST.get('descricao')
        valor_str = request.POST.get('valor').replace(',', '.')
        data = request.POST.get('data')
        status = request.POST.get('status')
        forma_pagamento = request.POST.get('forma_pagamento')

        try:
            valor = Decimal(valor_str)
        except ValueError:
            return render(request, 'financeiro/editar_receita.html', {
                'error': 'Formato de número inválido.',
                'receita': receita,
                'pacientes': pacientes,
                'produtos': produtos
            })

        receita.cliente = get_object_or_404(Paciente, id=cliente_id)
        receita.descricao = get_object_or_404(Produto, id=produto_id)
        receita.valor = valor
        receita.data = data
        receita.status = status
        receita.forma_pagamento = forma_pagamento
        receita.save()

        return redirect('cadastrar_receita')

    return render(request, 'financeiro/editar_receita.html', {
        'receita': receita,
        'pacientes': pacientes,
        'produtos': produtos
    })


def cadastrar_despesa(request):
    despesas = Despesa.objects.filter(usuario=request.user).order_by('data')
    hoje = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        data = request.POST.get('data', hoje)
        valor_str = request.POST.get('valor').replace(',', '.')

        try:
            valor = Decimal(valor_str)
        except ValueError:
            messages.error(request, 'Formato de número inválido.')
            return render(request, 'cadastrar_despesa.html', {
                'despesas': despesas,
                'hoje': hoje
            })

        Despesa.objects.create(
            descricao=descricao,
            data=data,
            valor=valor,
            usuario=request.user
        )
        messages.success(request, 'Despesa cadastrada com sucesso.')
        return redirect('cadastrar_despesa')

    return render(request, 'cadastrar_despesa.html', {
        'despesas': despesas,
        'hoje': hoje
    })


def editar_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        valor_str = request.POST.get('valor').replace(',', '.')
        try:
            valor = Decimal(valor_str)
        except ValueError:
            messages.error(request, 'Formato de número inválido.')
            return redirect('editar_despesa', despesa_id=despesa_id)

        despesa.descricao = descricao
        despesa.data = data
        despesa.valor = valor
        despesa.save()

        messages.success(request, 'Despesa atualizada com sucesso.')
        return redirect('cadastrar_despesa')

    return render(request, 'editar_despesa.html', {'despesa': despesa})


def excluir_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, id=despesa_id)

    if request.method == 'POST':
        despesa.delete()
        messages.success(request, 'Despesa excluída com sucesso.')
        return redirect('cadastrar_despesa')

    return redirect('cadastrar_despesa')


def relatorios(request):
    receitas = Receita.objects.filter(usuario=request.user)
    despesas = Despesa.objects.filter(usuario=request.user)

    total_receitas = sum(receita.valor for receita in receitas)
    total_despesas = sum(despesa.valor for despesa in despesas)

    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        receitas = Receita.objects.filter(
            data__range=[data_inicio, data_fim], usuario=request.user)
        despesas = Despesa.objects.filter(
            data__range=[data_inicio, data_fim], usuario=request.user)

        total_receitas = sum(receita.valor for receita in receitas)
        total_despesas = sum(despesa.valor for despesa in despesas)

    context = {
        'receitas': receitas,
        'despesas': despesas,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
    }
    return render(request, 'relatorios.html', context)
