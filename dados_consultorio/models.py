from django.db import models


class DadosConsultorio(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    usuario = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nome
