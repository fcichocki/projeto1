from django.contrib import admin
from .models import Agendamento


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'data', 'horario',
                    'profissional', 'convenio', 'status', 'data_hora_sistema']
    list_filter = ['data', 'profissional', 'status']
    search_fields = ['nome', 'telefone', 'email']
    ordering = ['data', 'horario']


admin.site.register(Agendamento, AgendamentoAdmin)
