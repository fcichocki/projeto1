from django.db import models
from convenios.models import Convenio


class Profissional(models.Model):
    # Adicionando campo 'id' como chave primária
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    cpf_cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    convenios = models.ManyToManyField(Convenio, blank=True)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nome
