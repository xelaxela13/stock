(function ($) {
    $(function () {
        // order type
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
        // end order type

        // get product available
        setTimeout(function () {
            let add_row = $('.add-row a');
            add_row.click(function () {
                setTimeout(function () {
                    let product = $('select[name*="order_items-"]');
                    product.change(function () {
                        let product_id = $(this).val(),
                            field_available_for_sale = $(this).parents('.dynamic-order_items').find('.field-available_for_sale p');
                        $.get('/stock/get-available-product/',
                            {'product_id': product_id},
                            function (data) {
                                field_available_for_sale.html(data['available']);
                            })
                    })
                }, 1000)
            })
        }, 1000);


        // end get product available
    })
})(django.jQuery);