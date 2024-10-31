$(document).ready(function () {
    $('#send-comment').click(function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Retrieve the selected rating
        let selectedRating = $('#product-review-form-rating-select').val();

        // Retrieve the comment text
        let commentText = $('#comment-text');
        let productSlug = commentText.data('slug');

        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        // Send data via AJAX
        $.ajax({
            type: 'POST',
            url: `${window.location.origin}/products/detail/${productSlug}/comment/`,
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            data: {
                'slug': productSlug,
                'text': commentText.val(),
                'rating': selectedRating,
            },
            success: function (response) {
                console.log('Comment submitted successfully:', response);
                if(response.message) {
                    alert(response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error submitting comment:', error);
            }
        });

        // Clear the textarea after logging
        $('#comment-text').val('');
    });
});