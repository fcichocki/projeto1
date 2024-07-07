from django.db import models
from profissionais.models import Profissional
# Importe o modelo Convenio do seu aplicativo
from convenios.models import Convenio


class Agendamento(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    data = models.DateField()
    horario = models.TimeField()
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    # Adicionando o campo convenio permitindo valor nulo
    convenio = models.ForeignKey(
        Convenio, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    data_hora_sistema = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.data} {self.horario}"
