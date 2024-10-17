$(document).ready(function () {
    $('.action-btn-wishlist').click(function () {
        let productSlug = $(this).data('slug');
        let icon = $(this).find('i');

        $.ajax({
            url: `${window.location.origin}/like/`,
            type: 'GET',
            data: {
                'slug': productSlug
            },
            success: function (response) {
                if(response.user) {
                    $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('شما ابتدا باید در سایت یک اکانت بسازید');
                } else {
                    if (response.liked) {
                        console.log('Liked successfully');
                        icon.removeClass('fa-heart-o').addClass('fa-heart');
                        $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('به لیست علاقه مندی ها اضافه شد');
                    } else {
                        console.log('Failed to like');
                        icon.removeClass('fa-heart').addClass('fa-heart-o');
                        $('#action-WishlistModal-' + productSlug + ' .modal-action-messages').text('از لیست علاقه مندی ها حذف شد');
                    }
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});