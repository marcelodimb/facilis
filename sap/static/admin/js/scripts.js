$(function () {
    // Cria as mascaras para os campos de telefones e para os CPF e CNPJ
    $('#id_telefone_fixo').mask('(00)0000-0000', {placeholder: "(__)____-____", clearIfNotMatch: true});
    $('#id_telefone_celular').mask('(00)00000-0000', {placeholder: "(__)_____-____", clearIfNotMatch: true});
    $('#id_tipo_documento').on('change', function (){
        if(parseInt($(this).val()) === 1) {
            $('#id_tipo_documento_conteudo').mask('000.000.000-00', {placeholder: "___.___.___-__", clearIfNotMatch: true});
        } else if(parseInt($(this).val()) === 2) {
            $('#id_tipo_documento_conteudo').mask('00.000.000/0000-00', {placeholder: "__.___.___/____-__", clearIfNotMatch: true});
        } else {
            $('#id_tipo_documento_conteudo').attr('placeholder', '');
            $('#id_tipo_documento_conteudo').val('');
        }
        $('#id_tipo_documento_conteudo').focus();
    });

    Suit.after_inline.register('my_unique_func_name', function(inline_prefix, row){
        // Trata do evento de adicionar exigências
        if (inline_prefix === 'exigencia_set') {
            // Desabilita o campo de atendida
            row.find('.form-row.field-atendida').hide();
        }
    });
});
