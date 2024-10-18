$(document).ready(function () {
    $('.action-btn-cart').click(function () {
        let productSlug = $(this).data('slug');
        let quantity = 1;
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrfToken);

        $.ajax({
            url: `${window.location.origin}/cart/add/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            data: {
                'slug': productSlug,
                'quantity': quantity
            },
            success: function (response) {
                if(response.existed) {
                    $('.product-' + productSlug).remove()
                }
                $('.aside-cart-product-list').append(response.page);
                $('#cart-total-price').text(response.total_price + ' تومان');
                // $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('از لیست علاقه مندی ها حذف شد');
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    $('.custom-add').click(function () {
        let productSlug = $(this).data('slug');
        let quantity = $('#quick-quantity-' + productSlug).val();
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log(csrfToken);
        $.ajax({
            url: `${window.location.origin}/cart/add/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {
                'slug': productSlug,
                'quantity': quantity
            },
            success: function (response) {
                if(response.existed) {
                    $('.product-' + productSlug).remove()
                }
                $('.aside-cart-product-list').append(response.page);
                $('#cart-total-price').text(response.total_price + ' تومان');
                // $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('از لیست علاقه مندی ها حذف شد');
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});