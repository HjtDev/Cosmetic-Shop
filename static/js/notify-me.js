$(document).ready(function () {
    $('.notify-me').click(function (e) {
        e.preventDefault();
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let slug = $(this).data('slug');
        let button = $(this);

        $.ajax({
            url: `${window.location.origin}/products/detail/notify-me/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {
                'slug': slug
            },
            success: function (response) {
                if(response.ok) {
                    $('#action-NotifyMeModal-' + slug + ' .modal-action-messages').text(response.message);
                    if(response.flag) {
                        button.text('در لیست اطلاع رسانی');
                    } else {
                        button.text('موجود شد اطلاع بده');
                    }
                }
            },
            error: function (response) {
                $('#action-NotifyMeModal-' + slug + ' .modal-action-messages').text(response.error);
            }
        });
    })
});