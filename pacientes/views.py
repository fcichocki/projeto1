from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from arquivos.models import Arquivo
from observacoes.models import Observacao
from django.views.decorators.http import require_POST
from atestados.models import Atestado, AtestadoPaciente

from .models import Paciente
from termo_consentimento.models import ConsentimentoPaciente, TermoConsentimento
from django.contrib import messages
from anamnese.models import Anamnese, AnamnesePaciente
from prescricoes.models import Prescricao
from anotacoes.models import Anotacao


from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_paciente(request):
    usuario_logado = request.user.username  # Obtém o nome do usuário logado

    if request.method == 'POST':
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')
        cep = request.POST.get('cep')

        Paciente.objects.create(
            nome=nome, sexo=sexo, cpf=cpf, telefone=telefone,
            email=email, endereco=endereco, cep=cep, usuario=usuario_logado
        )
        return redirect('cadastrar_paciente')

    # Filtrar pacientes pelo usuário logado
    pacientes = Paciente.objects.filter(usuario=usuario_logado)
    return render(request, 'cadastrar_paciente.html', {'pacientes': pacientes})


def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('cadastrar_paciente')


@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.nome = request.POST.get('nome')
        paciente.sexo = request.POST.get('sexo')
        paciente.cpf = request.POST.get('cpf')
        paciente.telefone = request.POST.get('telefone')
        paciente.email = request.POST.get('email')
        paciente.endereco = request.POST.get('endereco')
        paciente.cep = request.POST.get('cep')
        paciente.usuario = request.user.username  # Salva o nome de usuário
        paciente.save()

        return redirect('cadastrar_paciente')

    return render(request, 'editar_paciente.html', {'paciente': paciente})


def detalhes_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    termos = ConsentimentoPaciente.objects.filter(paciente=paciente)
    anamneses_paciente = AnamnesePaciente.objects.filter(paciente=paciente)
    prescricoes = Prescricao.objects.filter(
        paciente=paciente).order_by('-data_hora')
    atestados_paciente = AtestadoPaciente.objects.filter(
        paciente=paciente).order_by('-data_hora')
    arquivos_paciente = Arquivo.objects.filter(paciente=paciente)
    anotacao, created = Anotacao.objects.get_or_create(paciente=paciente)

    # Assegura-se de que estamos passando o texto das anotações corretamente.
    # 'anotacao_texto' será uma string vazia se a anotação for criada agora (ou seja, ainda não tiver texto).
    anotacao_texto = anotacao.anotacoes if anotacao and hasattr(
        anotacao, 'anotacoes') else ''

    return render(request, 'detalhes_paciente.html', {
        'paciente': paciente,
        'termos': termos,
        'anamneses_paciente': anamneses_paciente,
        'prescricoes': prescricoes,
        'atestados_paciente': atestados_paciente,
        'arquivos_paciente': arquivos_paciente,
        'anotacao_texto': anotacao_texto  # Passa o texto das anotações ao template
    })


@login_required
def cadastrar_termo_consentimento(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Filtrar termos de consentimento pelo usuário logado
    todos_termos_consentimento = TermoConsentimento.objects.filter(
        usuario=request.user.username)

    if request.method == 'POST':
        termo_id = request.POST.get('termo_consentimento')
        termo_consentimento = get_object_or_404(
            TermoConsentimento, id=termo_id)
        ConsentimentoPaciente.objects.create(
            paciente=paciente, termo_consentimento=termo_consentimento)
        return redirect('detalhes_paciente', id=paciente_id)

    return render(request, 'cadastrar_termo_consentimento.html', {
        'paciente': paciente,
        'todos_termos_consentimento': todos_termos_consentimento
    })


def excluir_termo_consentimento(request, id):
    consentimento = get_object_or_404(ConsentimentoPaciente, id=id)

    if request.method == 'POST':
        consentimento.delete()
        messages.success(
            request, 'Termo de consentimento removido com sucesso.')
        return redirect('detalhes_paciente', id=consentimento.paciente.id)

    return redirect('detalhes_paciente', id=consentimento.paciente.id)


def anamnese_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    todas_anamneses = Anamnese.objects.filter(usuario=request.user)
    respostas_anamneses = AnamnesePaciente.objects.filter(paciente=paciente)

    # Cria um dicionário para mapear as respostas de anamnese pelo id da anamnese
    respostas_dict = {
        resposta.anamnese.id: resposta for resposta in respostas_anamneses}

    # Atribuir as respostas diretamente aos objetos de anamnese para acesso fácil no template
    for anamnese in todas_anamneses:
        anamnese.resposta = respostas_dict.get(anamnese.id, None)

    if request.method == 'POST':
        for anamnese in todas_anamneses:
            confirmacao_input = request.POST.get(f'confirmacao_{anamnese.id}')
            confirmacao = confirmacao_input == 'Sim'
            observacoes = request.POST.get(f'observacoes_{anamnese.id}', '')

            AnamnesePaciente.objects.update_or_create(
                paciente=paciente,
                anamnese=anamnese,
                defaults={'confirmacao': confirmacao,
                          'observacoes': observacoes}
            )
        return redirect('detalhes_paciente', id=paciente_id)

    return render(request, 'anamnese_paciente_selecionado.html', {
        'paciente': paciente,
        'todas_anamneses': todas_anamneses
    })


def excluir_prescricao(request, prescricao_id):
    if request.method == 'POST':
        prescricao = get_object_or_404(Prescricao, id=prescricao_id)
        paciente_id = prescricao.paciente.id  # Guarda o ID do paciente antes de excluir
        prescricao.delete()
        messages.success(request, "Prescrição excluída com sucesso.")
        return redirect('detalhes_paciente', id=paciente_id)
    else:
        messages.error(request, "Método inválido para esta operação.")
        return redirect('detalhes_paciente', id=request.user.id)


def criar_prescricao(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        # Corrigido para capturar 'prescricaoTexto'
        texto_prescricao = request.POST.get('prescricaoTexto')
        if texto_prescricao:  # Verifica se o campo não é vazio
            Prescricao.objects.create(
                paciente=paciente,
                prescricoes=texto_prescricao
            )
            return redirect('detalhes_paciente', id=paciente_id)
        else:
            # Retorne um erro ou mensagem se a prescrição estiver vazia
            pass

    return render(request, 'detalhes_paciente.html', {'paciente': paciente})


def novo_atestado(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    atestados = Atestado.objects.all()  # Obtém todos os atestados para o dropdown

    # Preparando o texto pré-carregado para a área de texto do atestado
    texto_pre_carregado = f"Nome: {paciente.nome}\nCPF: {paciente.cpf}\nEmail: {paciente.email}\nTelefone: {
        paciente.telefone}\n\n\nATESTADO:\n\nAtesto para os devidos fins, que o paciente acima descrito\n\n\n"

    if request.method == 'POST':
        atestado_texto = request.POST.get('atestado')

        # Cria um novo atestado no banco de dados
        AtestadoPaciente.objects.create(
            paciente=paciente,
            atestado=atestado_texto  # Salvando o campo correto
        )

        # Redireciona para a página de detalhes do paciente após o cadastro
        return redirect('detalhes_paciente', id=paciente_id)

    # Se o método não for POST, exibe o formulário de novo atestado
    return render(request, 'novo_atestado.html', {
        'paciente': paciente,
        'atestados': atestados,  # Passa os atestados para o template
        'texto_pre_carregado': texto_pre_carregado
    })


@require_POST
def excluir_atestado(request, atestado_id):
    atestado = get_object_or_404(AtestadoPaciente, id=atestado_id)
    paciente_id = atestado.paciente.id
    atestado.delete()
    return redirect('detalhes_paciente', id=paciente_id)


def observacoes_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    observacoes = Observacao.objects.filter(paciente=paciente)

    if request.method == 'POST':
        texto_observacao = request.POST.get('observacoes', '').strip()
        if texto_observacao:
            Observacao.objects.create(
                paciente=paciente, observacoes=texto_observacao)
            # Redirecionar para a mesma página para atualizar a lista de observações
            return redirect('observacoes_paciente', paciente_id=paciente_id)

    return render(request, 'observacoes.html', {'paciente': paciente, 'observacoes': observacoes})


def listar_observacoes(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    observacoes_paciente = Observacao.objects.filter(paciente=paciente)
    context = {
        'paciente': paciente,
        'observacoes_paciente': observacoes_paciente,
    }
    return render(request, 'nome_do_template.html', context)


@require_POST
def excluir_observacao(request, observacao_id):
    observacao = get_object_or_404(Observacao, id=observacao_id)
    paciente_id = observacao.paciente.id
    observacao.delete()
    return redirect('observacoes_paciente', paciente_id=paciente_id)


def adicionar_arquivo(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        # Usa getlist para pegar todos os arquivos
        arquivos = request.FILES.getlist('arquivos')

        for arquivo in arquivos:
            Arquivo.objects.create(paciente=paciente, arquivo=arquivo)

        messages.success(request, 'Arquivos carregados com sucesso.')
        return redirect('detalhes_paciente', id=paciente_id)

    return render(request, 'adicionar_arquivo.html', {'paciente': paciente})


def excluir_arquivo(request, arquivo_id):
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)
    # Assumindo que o arquivo tem uma chave estrangeira para paciente
    paciente_id = arquivo.paciente.id

    if request.method == 'POST':
        arquivo.delete()  # Exclui o arquivo do banco de dados
        return redirect('detalhes_paciente', id=paciente_id)

    # Se não for POST, redirecione de volta para a página de detalhes do paciente, ou mostre uma página de confirmação
    return redirect('detalhes_paciente', id=paciente_id)


@login_required
def buscar_pacientes(request):
    query = request.GET.get('q', '')
    usuario_logado = request.user.username  # Obtém o nome do usuário logado
    pacientes = Paciente.objects.filter(
        nome__icontains=query, usuario=usuario_logado)
    return render(request, 'cadastrar_paciente.html', {'pacientes': pacientes, 'query': query})
