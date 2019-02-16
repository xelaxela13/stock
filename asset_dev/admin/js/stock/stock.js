(function ($) {
    $(function () {
        let order_type_select = $('#id_type'),
            field_user = $('.fieldBox.field-user');

        function is_order_type(obj) {
            if (obj.val() === '0') {
                field_user.hide();
            } else {
                field_user.show();
            }
        }
        is_order_type(order_type_select);
        order_type_select.change(function () {
            is_order_type($(this));
        });
    })
})(django.jQuery);