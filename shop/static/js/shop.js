$(function() {
    $('.add-order-item-to-cart').on('click', function(event) {
        var $form = $(this).closest('form');
        $.ajax({
            type:"GET",
            url: "/shop/add_to_cart",
            data:{
                'model': $form.find('input[name="model"]').val(),
                'color': $form.find('select[name="color"]').val(),
                'material': $form.find('select[name="material"]').val(),
                'cutter': $form.find('select[name="cutter"]').val()
            }
        })
    });
    
    $('.order-item-form').on('submit', function (e) {
        e.preventDefault();
        return false;
    });

    $('.order-item-form select[name="material"]').change(function (e) {
        var $form = $(this).closest('form');
        $.ajax({
            type:"GET",
            url: "/shop/calc_price",
            data:{
                'model': $form.find('input[name="model"]').val(),
                'material': $(this).val(),
            },
            success: function (data, type, xhr) {
                $form.find('.price').text(data.price + ' руб.')
            }
        })
    })
});

