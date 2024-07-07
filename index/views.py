
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'home.html')


def financeiro(request):
    return render(request, 'financeiro.html')


def configuracoes(request):
    return render(request, 'configuracoes.html')
