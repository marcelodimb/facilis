# -*- coding: utf-8 -*-
from django.db import models

class Procedimento(models.Model):
	interessado = models.CharField(max_length=128, unique=True)
	email = models.EmailField(max_length=128, unique=True, null=True, blank=True)
	telefone = models.CharField(max_length=11, null=True, blank=True)
	observacoes = models.TextField(null=True, blank=True, verbose_name="Observações")
	criado_em = models.DateTimeField(auto_now_add=True, editable=False, null=True)
	modificado_em = models.DateTimeField(auto_now=True, editable=False, null=True)

	def __unicode__(self):
		return self.interessado

	class Meta:
		verbose_name_plural = "procedimentos"
