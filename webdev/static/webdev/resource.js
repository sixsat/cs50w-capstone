document.addEventListener('DOMContentLoaded', function() {
    form = document.querySelector('#comment-form');
    if (form !== null) {
        form.onsubmit = () => add_comment(document.querySelector('#resource-id').value);
    }
});

function add_comment(resource_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const element_comment = document.querySelector('#new-comment');

    // Ensure comment is not empty
    if (element_comment.value.trim() === '') {
        return false;
    }

    fetch(`/resource/${resource_id}/comment`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            comment: element_comment.value
        })
    })
    .then(response => response.json())
    .then(result => {
        const element = document.createElement('div');
        element.classList.add('card', 'mb-3');
        element.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${result['username']}</h5>
                <p class="card-text">${element_comment.value}</p>
                <p class="card-text"><small class="text-muted">${result['timestamp']}</small></p>
            </div>
        `;
        document.querySelector('#comments').append(element);

        // Show response message
        const element_message = document.querySelector('#message');
        element_message.innerHTML = '';
        element_message.className = '';
        if (result['error']) {
            element_message.classList.add('alert', 'alert-danger', 'alert-dismissible', 'fade', 'show');
            element_message.innerHTML = result['error'];
        } else {
            element_message.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
            element_message.innerHTML = result['message'];
        }
        element_message.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    
        element_comment.value = '';
    })
    .catch(error => {
        console.log(error);
    });

    // Prevent default submission
    return false;
}