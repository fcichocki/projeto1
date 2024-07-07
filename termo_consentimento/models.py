from django.utils import timezone
from django.db import models
from pacientes.models import Paciente


class TermoConsentimento(models.Model):
    nome = models.CharField(max_length=50)
    termo_consentimento = models.TextField(max_length=5000)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nome


class ConsentimentoPaciente(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name='consentimentos')
    termo_consentimento = models.ForeignKey(
        TermoConsentimento, on_delete=models.CASCADE, related_name='consentimentos_pacientes')

    data_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.paciente.nome} - {self.termo_consentimento.nome}"
