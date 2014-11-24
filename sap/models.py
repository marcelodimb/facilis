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
    nome_parte = models.CharField(max_length=128, unique=True, verbose_name="Nome da parte")
    email = models.EmailField(max_length=128, unique=True, null=True, blank=True)
    telefone_fixo = models.CharField(max_length=14, null=True, blank=True, help_text="Informe apenas números")
    telefone_celular = models.CharField(max_length=15, null=True, blank=True, help_text="Informe apenas números")
    tipo_documento = models.IntegerField(max_length=1, verbose_name="Tipo de documento")
    tipo_documento_conteudo = models.CharField(max_length=18, verbose_name="", help_text="Informe apenas números")
    assunto = models.ForeignKey(Assunto)
    situacao = models.ForeignKey(Situacao, default=1, verbose_name="Situação")
    auditor_responsavel = models.ForeignKey(User, verbose_name="Auditor responsável", related_name="user_auditor_responsavel")
    observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
    inspetoria = models.ForeignKey(Inspetoria, editable=False)
    criado_por = models.ForeignKey(User, editable=False, null=True, related_name="user_criado_por")
    modificado_por = models.ForeignKey(User, editable=False, null=True, related_name="user_modificado_por")
    criado_em = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Data de abertura")
    modificado_em = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __unicode__(self):
        return self.nome_parte

    def display_criado_em(self):
        return self.criado_em.strftime('%d/%m/%Y - %H:%M')

    def display_id(self):
        return "{0:06d}".format(self.id)

    def display_auditor_responsavel(self):
        auditor_responsavel = ""
        try:
            u = User.objects.get(username=self.auditor_responsavel)
            auditor_responsavel = u.get_full_name()
        except:
            pass

        return auditor_responsavel

    class Meta:
        verbose_name_plural = "procedimentos"

    display_id.admin_order_field = 'id'
    display_id.short_description = 'N° protocolo'

    display_criado_em.admin_order_field = 'criado_em'
    display_criado_em.short_description = 'Data de abertura'

    display_auditor_responsavel.admin_order_field = 'auditor_responsavel'
    display_auditor_responsavel.short_description = 'Auditor responsável'


class Exigencia(models.Model):
    procedimento = models.ForeignKey(Procedimento)
    conteudo = models.TextField(null=True, blank=True, verbose_name="Conteúdo")
    atendida = models.BooleanField(blank=True, default=False)
    criado_em = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modificado_em = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __unicode__(self):
        return self.conteudo

    class Meta:
        verbose_name = "exigência"
        verbose_name_plural = "exigências"


class Usuario_Inspetoria(models.Model):
    user = models.OneToOneField(User)
    inspetoria = models.ForeignKey(Inspetoria)


class GrupoTrabalho(models.Model):
    nome = models.CharField(max_length=128, unique=True)
    assunto = models.OneToOneField(Assunto, unique=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name="Grupo de trabalho"
        verbose_name_plural="grupos de trabalho"


class GrupoTrabalhoAuditor(models.Model):
    grupo_trabalho = models.ForeignKey(GrupoTrabalho)
    auditor = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.auditor)

    class Meta:
        verbose_name="Auditor do grupo de trabalho"
        verbose_name_plural="Auditores do grupo de trabalho"
