# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.db.models import Q

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from .models import Assunto, Exigencia, GrupoTrabalho, GrupoTrabalhoAuditor, Inspetoria, Procedimento, Situacao, Usuario_Inspetoria
from .forms import ExigenciaForm, GrupoTrabalhoAuditorForm, ProcedimentoForm


# Funcao de gerar um arquivo PDF contendo os dados do procedimento solicitado
def print_procedimento(self, request, queryset):
    # Verifica se foram selecionados mais de 1 procedimento
    if len(queryset) > 1:
        self.message_user(request, "Selecione apenas 1 procedimento.")
    else:
        doc = SimpleDocTemplate("simple_table.pdf", pagesize=A4)

        style_sheet = getSampleStyleSheet()
        style_sheet.add(ParagraphStyle(
            name='title_style',
            leading=24,
            fontSize=12,
            spaceBefore=24
        ))
        style_sheet.add(ParagraphStyle(
            name='paragraph_procedimento',
            fontSize=8
        ))
        style_sheet.add(ParagraphStyle(
            name='paragraph_exigencias',
            fontSize=8,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletIndent=5
        ))

        # Container para os elementos flutuantes
        elements = []

        title_report = Paragraph('Serviço de Acompanhamento de processos', style_sheet["title_style"])
        elements.append(title_report)

        # Recupera o procedimento solicitado
        nome_parte = queryset[0].nome_parte
        codigo = "{0:06d}".format(queryset[0].id)
        email = queryset[0].email or "-"
        telefone_fixo = queryset[0].telefone_fixo or "-"
        telefone_celular = queryset[0].telefone_celular or "-"
        tipo_documento = 'CPF' if queryset[0].tipo_documento == 1 else 'CNPJ'
        tipo_documento_conteudo = queryset[0].tipo_documento_conteudo
        assunto = str(queryset[0].assunto)
        situacao = str(queryset[0].situacao)
        auditor_responsavel = queryset[0].auditor_responsavel.get_full_name()
        observacoes = queryset[0].observacoes or "-"
        criado_em = queryset[0].criado_em.strftime('%d/%m/%Y - %H:%M')
        criado_por = queryset[0].criado_por.get_full_name()
        modificado_em = queryset[0].modificado_em.strftime('%d/%m/%Y - %H:%M')
        modificado_por = queryset[0].modificado_por.get_full_name()

        data_procedimento = [
            ['Nome da parte:', nome_parte],
            ['Código:', codigo],
            ['E-mail:', email],
            ['Telefone fixo:', telefone_fixo],
            ['Telefone celular:', telefone_celular],
            [tipo_documento + ':', tipo_documento_conteudo],
            ['Assunto:', assunto],
            ['Situação', situacao],
            ['Auditor responsável:', auditor_responsavel],
            ['Criado em:', criado_em],
            ['Criado por:', criado_por],
            ['Modificado em:', modificado_em],
            ['Modificado por:', modificado_por],
            ['Observações:', Paragraph(observacoes, style_sheet["paragraph_procedimento"])]
        ]
        table_procedimento=Table(data_procedimento, colWidths=(None, 400))
        table_procedimento.setStyle(TableStyle([
            ('FONT',(0,0),(0,-1), 'Helvetica-Bold', 8),
            ('ALIGN',(0,0),(0,-1), 'RIGHT'),
            ('VALIGN',(0,0),(0,-1), 'TOP'),
            ('FONT',(1,0),(-1,-1), 'Helvetica', 8)
        ]))
        elements.append(table_procedimento)

        title_exigencias = Paragraph('Exigências', style_sheet["title_style"])
        elements.append(title_exigencias)

        # Recupera as exigencias do procedimento solicitado
        exigencias = Exigencia.objects.filter(procedimento=queryset[0].id)

        if exigencias:
            data_exigencias = []

            for exigencia in exigencias:
                data_exigencias.append(
                    [Paragraph(exigencia.conteudo, style_sheet["paragraph_exigencias"], bulletText='*'), 'Atendida' if exigencia.atendida else 'Não atendida']
                )
            table_exigencias=Table(data_exigencias, colWidths=(390, None))
            table_exigencias.setStyle(TableStyle([
                ('FONT',(0,0),(0,-1), 'Helvetica', 8),
                ('VALIGN',(0,0),(0,-1), 'TOP'),
                ('FONT',(1,0),(-1,-1), 'Helvetica', 8)
            ]))
            elements.append(table_exigencias)
        else:
            elements.append(Paragraph('Este procedimento não possui exigências.', style_sheet["paragraph_exigencias"]))

        # write the document to disk
        doc.build(elements)

print_procedimento.short_description = "Imprimir procedimento selecionado"

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
                if obj:
                    r = False

                    # Checa se existe alguma exigencia para o procedimento atual e exibe o campo de atendida
                    if Exigencia.objects.filter(procedimento=int(request.path.split('/')[4])).exists():
                        r = True

                    return args if r else ()

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


class AuditorResponsavelListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Auditor Responsável'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'auditor_responsavel_id'

    def lookups(self, request, model_admin):
        user = User.objects.get(username=request.user.username)
        inspetoria = user.usuario_inspetoria.inspetoria

        # Pega o objeto referente ao grupo de Auditores(id=1)
        group = Group.objects.get(id=1)

        # Retorna a lista com os nomes dos membros do grupo
        auditores = group.user_set.all().filter(usuario_inspetoria__inspetoria=inspetoria.id).order_by('first_name', 'last_name', 'username')

        list = []

        for a in auditores:
            list.append((a.id, a.get_full_name()))

        return list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(auditor_responsavel_id=self.value())

        return queryset


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
    actions = (print_procedimento,)
    inlines = (ExigenciaInline,)
    list_display = ('display_id', 'nome_parte', 'display_auditor_responsavel', 'situacao', 'display_criado_em',)
    list_display_links = ('display_id', 'nome_parte', 'display_auditor_responsavel', 'situacao', 'display_criado_em',)
    list_filter = ('criado_em', 'modificado_em', 'situacao', AuditorResponsavelListFilter,)
    ordering = ('-id', 'nome_parte', 'auditor_responsavel', 'situacao', '-criado_em',)
    search_fields = ('nome_parte',)

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

        # Verifica se o usuario informou alguma exigencia e altera a situação para 'Em exigência'
        if has_exigencia(request):
            obj.situacao = Situacao.objects.get(id=2)
        else:
            # Verifica se o usuario solicitou concluir o procedimento ou não
            if 'situacao' in request.POST:
                if int(request.POST['situacao']) == 3:
                    obj.situacao = Situacao.objects.get(id=3)
                else:
                    obj.situacao = Situacao.objects.get(id=1)
            else:
                obj.situacao = Situacao.objects.get(id=1)

        u = User.objects.get(username=request.user.username)
        inspetoria = u.usuario_inspetoria.inspetoria
        obj.inspetoria = inspetoria

        if getattr(obj, 'criado_por', None) is None:
            obj.criado_por = request.user
        obj.modificado_por = request.user
        obj.save()

    @register.inclusion_tag('admin/submit_line.html', takes_context=True)
    def submit_row(context):
        ctx = original_submit_row(context)
        ctx.update({
            'readonly': context.get('readonly') or False,
        })
        return ctx

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        try:
            # Torna o formulário apenas para leitura caso a situação do procedimento esteja 'Concluído'
            p = Procedimento.objects.get(id=object_id)
            situacao = p.situacao_id

            if situacao == 3:
                extra_context['readonly'] = True
        except:
            pass

        return super(ProcedimentoAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'auditor_responsavel':
            # Usuário logado
            u = User.objects.get(username=request.user.username)

            # Inspetoria do usuário atual
            inspetoria = u.usuario_inspetoria.inspetoria

            try:
                # Pega o objeto referente ao grupo de auditores(id=1)
                group = Group.objects.get(id=1)

                # Retorna apenas a lista de auditores da inspetoria do usuário logado
                kwargs["queryset"] = group.user_set.all().filter(usuario_inspetoria__inspetoria=inspetoria.id).order_by('first_name', 'last_name', 'username')
            except:
                pass

            field = super(ProcedimentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

            # Formata o nome de exibição para o nome completo ao invés do username
            field.label_from_instance = self.get_user_label

            return field

        if db_field.name == 'situacao':
            try:
                p = Procedimento.objects.get(id=int(request.path.split('/')[4]))

                situacao_id = p.situacao_id

                # Define as possiveis situacoes a serem exibidas
                # Se o procedimento está 'Em análise', exibir apenas
                # 'Em análise'(id=1) e 'Concluído'(id=3)
                if situacao_id == 1:
                    kwargs["queryset"] = Situacao.objects.filter(Q(id=1) | Q(id=3))

                # Se o procedimento está 'Em exigência', exibir apenas
                # 'Em exigência'(id=2) e 'Concluído'(id=3)
                elif situacao_id == 2:
                    kwargs["queryset"] = Situacao.objects.filter(Q(id=2) | Q(id=3))

                # Se o procedimento está 'Concluído', exibir apenas 'Concluído'(id=3)
                else:
                    kwargs["queryset"] = Situacao.objects.filter(id=3)

            except:
                # Define a situação como 'Em análise'(id=1)
                kwargs["queryset"] = Situacao.objects.filter(id=1)
                pass

        return super(ProcedimentoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_user_label(self, user):
        return user.get_full_name()

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
