$(document).ready(function(){
    $('.modal-form').on('click', function() {
        var url = $(this).data('url');

        $.ajax({
            url: url,
            method: 'GET',
            success: function(response) {
                $('#modalForm .modal-body').html(response);
                $('#modalForm').modal('show');  // Tampilkan modal
            },
            error: function() {
                Swal.fire({
                    title: "Error",
                    text: "Error loading form.",
                    icon: "error"
                });
            }
        });
    });
    
    $('.save').on('click', function(event) {
        event.preventDefault();

        Swal.fire({
            title: "Are you sure ?",
            icon: "warning",
            showCancelButton: true,
            cancelButtonColor: "#d33",
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Save"
        }).then((result) => {
            if (result.isConfirmed) {
                var form = $('#modalForm form');
                var url = form.attr('action');
                var data = form.serialize();
                var csrfToken = getCookie('csrftoken');
                
                $.ajax({
                    url: url,
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken  // Add CSRF token to header
                    },
                    data: data,
                    success: function(response) {
                        Swal.fire({
                            title: response.title,
                            text: response.message,
                            icon: response.icon
                        }).then(() => {
                            if (response.status)
                                window.location.href = response.redirect;
                        });
                    },
                    error: function() {
                        Swal.fire({
                            title: "Error",
                            text: "Error saving data.",
                            icon: "error"
                        });    
                    }
                });
            }
        });
    })

    $('.delete').on('click', function(event) {
        event.preventDefault();

        Swal.fire({
            title: "Are you sure delete data ?",
            icon: "warning",
            showCancelButton: true,
            cancelButtonColor: "#d33",
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Yes"
        }).then((result) => {
            if (result.isConfirmed) {
                var url = $(this).data('url');
                var csrfToken = getCookie('csrftoken');

                $.ajax({
                    url: url,
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken  // Add CSRF token to header
                    },
                    success: function(response) {
                        Swal.fire({
                            title: response.title,
                            text: response.message,
                            icon: response.icon
                        }).then(() => {
                            if (response.status)
                                window.location.href = response.redirect;
                        });
                    },
                    error: function() {
                        Swal.fire({
                            title: "Error",
                            text: "Error delete data.",
                            icon: "error"
                        });    
                    }
                });
            }
        });
    })
})

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}