from django.db import models


class Anamnese(models.Model):
    anamnese = models.CharField(max_length=200)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.anamnese[:100]


class AnamnesePaciente(models.Model):
    paciente = models.ForeignKey(
        'pacientes.Paciente', on_delete=models.SET_NULL, null=True, blank=True)
    # Usando string para evitar importação circular
    anamnese = models.ForeignKey(
        'anamnese.Anamnese', on_delete=models.SET_NULL, null=True, blank=True)
    confirmacao = models.BooleanField(null=True, blank=True)
    observacoes = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # Pode precisar ajustar esta string de representação dependendo dos campos disponíveis
        return f"{self.paciente} - {self.anamnese}"
