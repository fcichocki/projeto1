from django.db import models
from profissionais.models import Profissional
from convenios.models import Convenio


class AgendaConvenio(models.Model):
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data = models.DateField()
    hora = models.TimeField()
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    inserido_por = models.CharField(max_length=100, blank=True, null=True)
    inserido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.data} {self.hora}"
