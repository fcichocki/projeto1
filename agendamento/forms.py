# forms.py
from django import forms
from .models import Agendamento, Profissional
from datetime import time

HORARIOS_DISPONIVEIS = [
    (time(8, 0), '08:00'),
    (time(9, 0), '09:00'),
    (time(10, 0), '10:00'),
]


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['nome', 'telefone', 'email', 'data',
                  'horario', 'profissional', 'convenio']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.Select(choices=HORARIOS_DISPONIVEIS),
            'profissional': forms.Select(),
            'convenio': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['convenio'].required = False
        if user:
            self.fields['profissional'].queryset = Profissional.objects.filter(
                usuario=user)
        if self.instance and self.instance.pk:
            self.fields['data'].initial = self.instance.data.strftime(
                '%Y-%m-%d')
