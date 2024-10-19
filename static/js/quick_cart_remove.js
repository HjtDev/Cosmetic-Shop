$(document).ready(function () {
    // Use event delegation to handle dynamically added elements
    $(document).on('click', '.quick-remove', function (event) {
        console.log('pressed');
        event.preventDefault(); // Prevent default anchor behavior

        // Get the slug from the data attribute
        let slug = $(this).data('slug'); // Extract slug from data attribute

        // Get CSRF token from the hidden input field
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        // Send AJAX request to remove the product
        $.ajax({
            url: `${window.location.origin}/cart/remove/`,  // Adjust this URL based on your URL configuration
            type: 'POST',
            contentType: 'application/json',  // Send as JSON
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            data: JSON.stringify({slug: slug}),  // Send slug as JSON
            success: function (response) {
                // Handle successful removal (e.g., update UI)
                $(`#product-${slug}`).remove();  // Remove the corresponding product list item
                $(`#cart-item-checkout-${slug}`).remove();  // Remove the corresponding product list item
                $('#cart-total-price').text(response.total_cost + ' تومان');  // Update total cost if needed
                $('#checkout-total-cost').text(response.total_cost + ' تومان');  // Update total cost if needed
            },
            error: function (xhr, status, error) {
                console.error('Error removing product');
                console.error(xhr, status, error);
            }
        });
    });
});