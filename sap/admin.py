# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from .models import Assunto, Exigencia, GrupoTrabalho, GrupoTrabalhoAuditor, Inspetoria, Procedimento, Situacao, Usuario_Inspetoria
from .forms import ExigenciaForm, GrupoTrabalhoAuditorForm, ProcedimentoForm


class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)


class InspetoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)


class SituacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)


class ExigenciaInline(admin.StackedInline):
    model = Exigencia
    form = ExigenciaForm
    extra = 0

    def get_fieldsets(self, request, obj=None):
        def if_editing(*args):
            if "atendida" in args:
                try:
                    obj = Exigencia.objects.get(procedimento=int(request.path.split('/')[4]))
                except:
                    obj = False
                    pass

            return args if obj else ()
        return (
            (None, {
                'classes': ('wide',),
                'fields': (
                    'conteudo',
                    if_editing('atendida',),
                )
            }),
        )


class GrupoTrabalhoAuditorInline(admin.StackedInline):
    model = GrupoTrabalhoAuditor
    form = GrupoTrabalhoAuditorForm
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'auditor',
            )
        }),
    )


class GrupoTrabalhoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    ordering = ['nome']
    search_fields = ['nome']
    inlines = (GrupoTrabalhoAuditorInline,)


class ProcedimentoAdmin(admin.ModelAdmin):
    form = ProcedimentoForm

    def get_fieldsets(self, request, obj=None):
        def if_editing(*args):
            # Trata da exibicao do campo situacao
            if "situacao" in args:
                # Confere se o procedimento é novo ou está sendo editado
                if obj:
                    try:
                        u = User.objects.get(username=request.user.username)

                        # Confere se o usuario é auditor para exibir a situacao
                        if u.groups.filter(id=1).exists():
                            r = True
                        else:
                            r = False
                    except:
                        r = False
                        pass
                    return args if r else ()

            return args if obj else ()

        return (
            (None, {
                'classes': ('wide',),
                'fields': (
                    'nome_parte',
                    'email',
                    'telefone_fixo',
                    'telefone_celular',
                    ('tipo_documento', 'tipo_documento_conteudo'),
                    'assunto',
                    if_editing('situacao',),
                    'auditor_responsavel',
                    'observacoes',
                )
            }),
        )
    list_display = ('display_id', 'nome_parte', 'auditor_responsavel', 'situacao', 'display_criado_em',)
    list_display_links = ('display_id', 'nome_parte', 'auditor_responsavel', 'situacao', 'display_criado_em',)
    list_filter = ('criado_em', 'modificado_em', 'situacao',)
    ordering = ('-id', 'nome_parte', 'auditor_responsavel', 'situacao', '-criado_em',)
    search_fields = ('nome_parte',)
    inlines = (ExigenciaInline,)

    class Media:
        js = (
            'admin/js/jquery.mask.min.js',
            'admin/js/scripts.js',
        )

    # Redefine a consulta padrão para exibir apenas os procesimentos referentes à inspetoria pertencente do usuário
    def queryset(self, request):
        qs = super(ProcedimentoAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs
        else:
            u = User.objects.get(username=request.user.username)
            inspetoria = u.usuario_inspetoria.inspetoria

            return qs.filter(inspetoria=inspetoria)

    # Redefine o método de salvar para incluir o usuario que atualizou o último procedimento
    def save_model(self, request, obj, form, change):
        def has_exigencia(request):
            has_conteudo = False
            deleted_exigencias = 0
            initial_forms = int(request.POST['exigencia_set-INITIAL_FORMS'])
            total_forms   = int(request.POST['exigencia_set-TOTAL_FORMS'])

            # Checa quantos elementos foram solicitados para serem apagados
            for i in range(initial_forms):
                if ("exigencia_set-%s-DELETE" % i) in request.POST:
                    deleted_exigencias += 1

            # Checa se o conteudo de alguma exigência está vazia
            for i in range(initial_forms, total_forms):
                if request.POST[("exigencia_set-%s-conteudo" % i)] != '':
                    has_conteudo = True

            return has_conteudo or (initial_forms > deleted_exigencias)

        # Verifica se o usuario informou alguma exigencia e altera a
        # situação para 'Em exigência' ou 'Em análise' caso contrário
        if has_exigencia(request):
            obj.situacao = Situacao.objects.get(id=2)
        else:
            obj.situacao = Situacao.objects.get(id=1)

        u = User.objects.get(username=request.user.username)
        inspetoria = u.usuario_inspetoria.inspetoria
        obj.inspetoria = inspetoria

        if getattr(obj, 'criado_por', None) is None:
            obj.criado_por = request.user
        obj.modificado_por = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        u = User.objects.get(username=request.user.username)
        inspetoria = u.usuario_inspetoria.inspetoria

        if db_field.name == 'auditor_responsavel':
            try:
                # Pega o objeto referente ao grupo de Auditores(id=1)
                group = Group.objects.get(id=1)

                # Retorna a lista com os nomes dos membros do grupo
                kwargs["queryset"] = group.user_set.all().filter(usuario_inspetoria__inspetoria=inspetoria.id).order_by('first_name', 'last_name', 'username')
            except:
                pass

        if db_field.name == 'situacao':
            try:
                Procedimento.objects.get(id=int(request.path.split('/')[4]))
                kwargs["queryset"] = Situacao.objects.all()
            except:
                # Define a situação como 'Em análise'(id=1)
                kwargs["queryset"] = Situacao.objects.filter(id=1)
                pass

        return super(ProcedimentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        ProcedimentoForm = super(ProcedimentoAdmin, self).get_form(request, obj, **kwargs)

        class ProcedimentoFormMetaClass(ProcedimentoForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ProcedimentoForm(*args, **kwargs)
        return ProcedimentoFormMetaClass


class Usuario_InspetoriaInline(admin.StackedInline):
    model = Usuario_Inspetoria
    can_delete = False
    verbose_name = "Inspetoria do usuário"
    verbose_name_plural = "Inspetoria do usuário"


# Define um novo UserAdmin
class UserAdmin(UserAdmin):
    inlines = (Usuario_InspetoriaInline, )

admin.site.register(Assunto, AssuntoAdmin)
admin.site.register(GrupoTrabalho, GrupoTrabalhoAdmin)
admin.site.register(Inspetoria, InspetoriaAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
admin.site.register(Situacao, SituacaoAdmin)

# Registra o novo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
