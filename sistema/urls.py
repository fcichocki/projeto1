
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from convenios.views import cadastrar_convenio, excluir_convenio
from profissionais.views import cadastrar_profissional, excluir_profissional, editar_profissional
from agenda.views import cadastrar_agenda, listar_agendamentos, excluir_agendamento, editar_agendamento
from agenda_convenio.views import cadastrar_agenda_convenio, listar_e_cadastrar_agendamentos_convenio, excluir_agendamento_convenio, editar_agendamento_convenio
from termo_consentimento.views import cadastrar_termo, editar_termo, excluir_termo, listar_termos
from pacientes.views import cadastrar_paciente, excluir_paciente, editar_paciente, detalhes_paciente, cadastrar_termo_consentimento, excluir_termo_consentimento, anamnese_paciente, excluir_prescricao, criar_prescricao, excluir_atestado, novo_atestado, observacoes_paciente, excluir_observacao, adicionar_arquivo, excluir_arquivo, buscar_pacientes, listar_observacoes
from dados_consultorio.views import cadastrar_dados_consultorio
from produtos.views import cadastrar_e_listar_produtos, excluir_produto, editar_produto
from financeiro.views import cadastrar_receita, excluir_receita, editar_receita, cadastrar_despesa, editar_despesa, excluir_despesa, relatorios
from index.views import index, financeiro, configuracoes
from anotacoes.views import ver_anotacoes, save_anotacoes
from anamnese.views import cadastrar_anamnese, excluir_anamnese, editar_anamnese
from autentica.views import custom_login_view, register, usuarios_cadastrados, edit_user, delete_user

from agendamento.views import agendar, horarios_disponiveis, agendar_adm, excluir_agendamento, editar_agendamento, horarios_disponiveis_edicao
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', index, name='index'),
    path('pg_financeiro', financeiro, name='financeiro'),
    path('pg_configuracoes', configuracoes, name='configuracoes'),




    path('cadastrar-convenio/', cadastrar_convenio, name='cadastrar_convenio'),
    path('excluir-convenio/<int:id_convenio>/',
         excluir_convenio, name='excluir_convenio'),
    path('cadastrar-profissional/', cadastrar_profissional,
         name='cadastrar_profissional'),
    path('excluir-profissional/<int:id_profissional>/',
         excluir_profissional, name='excluir_profissional'),
    path('editar-profissional/<int:id_profissional>/',
         editar_profissional, name='editar_profissional'),
    path('cadastrar-agenda/', cadastrar_agenda, name='cadastrar_agenda'),
    path('agendamentos/', listar_agendamentos, name='listar_agendamentos'),
    path('excluir-agendamento/<int:id_agendamento>/',
         excluir_agendamento, name='excluir_agendamento'),
    path('editar-agendamento/<int:id_agendamento>/',
         editar_agendamento, name='editar_agendamento'),
    path('cadastrar-agenda-convenio/', cadastrar_agenda_convenio,
         name='cadastrar_agenda_convenio'),
    path('agendamentos-convenio/', listar_e_cadastrar_agendamentos_convenio,
         name='listar_e_cadastrar_agendamentos_convenio'),
    path('agendamento-convenio/excluir/<int:id>/',
         excluir_agendamento_convenio, name='excluir_agendamento_convenio'),
    path('agendamento-convenio/editar/<int:id>/',
         editar_agendamento_convenio, name='editar_agendamento_convenio'),

    path('cadastrar_termo/', cadastrar_termo, name='cadastrar_termo'),
    path('editar_termo/<int:id>/', editar_termo, name='editar_termo'),
    path('excluir_termo/<int:id>/', excluir_termo, name='excluir_termo'),
    path('termos/', listar_termos, name='listar_termos'),

    path('cadastrar_pacientes/', cadastrar_paciente, name='cadastrar_paciente'),
    path('pacientes/excluir/<int:id>/',
         excluir_paciente, name='excluir_paciente'),

    path('editar_paciente/<int:id>/', editar_paciente, name='editar_paciente'),
    path('pacientes/detalhes/<int:id>/',
         detalhes_paciente, name='detalhes_paciente'),
    path('pacientes/<int:paciente_id>/cadastrar-termo/',
         cadastrar_termo_consentimento, name='cadastrar_termo_consentimento'),

    path('termo-consentimento/excluir/<int:id>/',
         excluir_termo_consentimento, name='excluir_termo_consentimento'),

    path('anamnese_paciente/<int:paciente_id>/anamnese/',
         anamnese_paciente, name='anamnese_paciente'),


    path('cadastro_consultorio/', cadastrar_dados_consultorio,
         name='cadastro_consultorio'),

    path('excluir_prescricao/<int:prescricao_id>/',
         excluir_prescricao, name='excluir_prescricao'),


    path('paciente_prescricao/<int:paciente_id>/nova-prescricao/',
         criar_prescricao, name='criar_prescricao'),

    path('excluir-atestado/<int:atestado_id>/',
         excluir_atestado, name='excluir_atestado'),

    path('paciente_atestado/<int:paciente_id>/novo-atestado/',
         novo_atestado, name='novo_atestado'),


    path('paciente_observacoes/<int:paciente_id>/observacoes/',
         observacoes_paciente, name='observacoes_paciente'),
    path('excluir_observacao_paciente/<int:observacao_id>/excluir/',
         excluir_observacao, name='excluir_observacao'),



    path('<int:paciente_id>/observacoes/',
         listar_observacoes, name='listar_observacoes'),




    path('produtos/', cadastrar_e_listar_produtos,
         name='cadastrar_e_listar_produtos'),

    path('produtos/excluir/<int:produto_id>/',
         excluir_produto, name='excluir_produto'),

    path('produtos/editar/<int:produto_id>/',
         editar_produto, name='editar_produto'),

    path('cadastrar_receita/',
         cadastrar_receita, name='cadastrar_receita'),

    path('financeiro/receitas/excluir/<int:receita_id>/',
         excluir_receita, name='excluir_receita'),

    path('financeiro/receitas/editar/<int:receita_id>/',
         editar_receita, name='editar_receita'),

    path('cadastrar_despesa/',
         cadastrar_despesa, name='cadastrar_despesa'),

    path('relatorios_financeiro/',
         relatorios, name='relatorios_financeiro'),

    path('financeiro/despesas/editar/<int:despesa_id>/',
         editar_despesa, name='editar_despesa'),
    path('financeiro/despesas/excluir/<int:despesa_id>/',
         excluir_despesa, name='excluir_despesa'),

    path('pacientes_arquivos/<int:paciente_id>/adicionar_arquivo/',
         adicionar_arquivo, name='adicionar_arquivo'),


    path('arquivos/excluir/<int:arquivo_id>/',
         excluir_arquivo, name='excluir_arquivo'),



    path('cadastrar_anamnese/', cadastrar_anamnese, name='cadastrar_anamnese'),
    path('excluir_anamnese/<int:id>/', excluir_anamnese, name='excluir_anamnese'),
    path('editar_anamnese/<int:id>/', editar_anamnese, name='editar_anamnese'),





    path('buscar_pacientes/', buscar_pacientes, name='buscar_pacientes'),

    path('paciente/<int:paciente_id>/anotacoes/',
         ver_anotacoes, name='ver_anotacoes'),

    path('paciente/<int:paciente_id>/save-anotacoes/',
         save_anotacoes, name='save_anotacoes'),


    # AGENDAMENTO

    path('agendar/', agendar, name='agendar'),
    path('horarios_disponiveis/', horarios_disponiveis,
         name='horarios_disponiveis'),

    path('agendar_adm/', agendar_adm, name='agendar_adm'),
    path('horarios_disponiveis/', horarios_disponiveis,
         name='horarios_disponiveis'),
    path('excluir_agendamento/<int:agendamento_id>/',
         excluir_agendamento, name='excluir_agendamento'),

    path('editar_agendamento/<int:agendamento_id>/',
         editar_agendamento, name='editar_agendamento'),

    path('horarios-disponiveis-edicao/', horarios_disponiveis_edicao,
         name='horarios_disponiveis_edicao'),


    # AUTENTICA

    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/index'), name='logout'),
    path('register/', register, name='register'),
    path('usuarios/', usuarios_cadastrados, name='usuarios_cadastrados'),
    path('usuarios/<int:user_id>/', usuarios_cadastrados,
         name='usuarios_cadastrados'),

    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change_form.html',
        success_url='/somewhere/'
    ), name='password_change'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
