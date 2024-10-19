$(document).ready(function () {
    // Initially disable the button
    $('.btn-place-order').prop('disabled', true);

    // Listen for changes on the checkbox
    $('#privacy').change(function () {
        if ($(this).is(':checked')) {
            // Enable the button if checked
            $('.btn-place-order').prop('disabled', false);
        } else {
            // Disable the button if not checked
            $('.btn-place-order').prop('disabled', true);
        }
    });
});