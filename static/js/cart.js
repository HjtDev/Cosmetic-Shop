$(document).ready(function () {
    $('.action-btn-cart').click(function () {
        let productSlug = $(this).data('slug');
        let quantity = 1;

        $.ajax({
            url: `${window.location.origin}/cart/add/`,
            type: 'GET',
            data: {
                'slug': productSlug,
                'quantity': quantity
            },
            success: function (response) {
                if(response.existed) {
                    $('.product-' + productSlug).remove()
                }
                $('.aside-cart-product-list').append(response.page);
                // $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('از لیست علاقه مندی ها حذف شد');
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});