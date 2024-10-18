$(document).ready(function () {
    $('.btn-update-cart').click(function (event) {
        event.preventDefault(); // Prevent default form submission if needed

        // Disable the button
        $(this).prop('disabled', true);

        // Initialize an array to hold slug and quantity pairs
        let cartItems = [];

        // Iterate over each quantity input field
        $('.quantity').each(function () {
            let slug = $(this).data('slug'); // Get the slug from the data attribute
            let quantity = $(this).val(); // Get the quantity value

            // Push the slug and quantity into the array
            cartItems.push({slug: slug, quantity: quantity});
        });

        if (cartItems.length === 0) {
            return;
        }

        // Get CSRF token from the hidden input field
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let data = JSON.stringify(cartItems);

        // Send all items to the server via AJAX
        $.ajax({
            url: `${window.location.origin}/cart/update/`,  // Adjust this URL based on your URL configuration
            type: 'POST',
            contentType: 'application/json',  // Send as JSON
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            data: data,  // Convert array to JSON string
            success: function (response) {
                $('.btn-update-cart').prop('disabled', false);
                $('#total-cart-cost').text(response.total_cost + ' تومان');

                // Update each item's price and total price in the DOM
                for (const slug in response.items) {
                    if (response.items.hasOwnProperty(slug)) {
                        const item = response.items[slug];
                        $(`#price-${slug}`).text(item.price + ' تومان');  // Update individual item price
                        $(`#total-${slug}`).text(item.total + ' تومان');  // Update total price for this item
                    }
                }
            },
            error: function (xhr, status, error) {
                console.log(xhr, status, error);
                $('.btn-update-cart').prop('disabled', false);  // Re-enable button on error
            }
        });
    });

    $('.remove').click(function (event) {
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
                $(`#product-row-${slug}`).remove();  // Remove the corresponding table row
                $('#total-cart-cost').text(response.total_cost + ' تومان');  // Update total cost if needed
            },
            error: function (xhr, status, error) {
                console.error('Error removing product');
                console.error(xhr, status, error);
            }
        });
    });
});