# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Assunto(models.Model):
    nome = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "assuntos"


class Inspetoria(models.Model):
    nome = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural="inspetorias"


class Situacao(models.Model):
    nome = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural="situações"


class Procedimento(models.Model):
    interessado = models.CharField(max_length=128, unique=True, verbose_name="Nome do interessado")
    email = models.EmailField(max_length=128, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    assunto = models.ForeignKey(Assunto)
    situacao = models.ForeignKey(Situacao, default=1)
    auditor_responsavel = models.ForeignKey(User, verbose_name="Auditor responsável")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    data_de_abertura = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modificado_em = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __unicode__(self):
        return self.interessado

    class Meta:
        verbose_name_plural = "procedimentos"


class Exigencia(models.Model):
    procedimento = models.ForeignKey(Procedimento)
    conteudo = models.TextField(null=True, blank=True, verbose_name="Conteúdo")
    atendida = models.BooleanField(blank=True)

    def __unicode__(self):
        return self.conteudo

    class Meta:
        verbose_name_plural = "exigências"
