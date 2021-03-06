document.addEventListener('DOMContentLoaded', function() {
    const form_comment = document.querySelector('#comment-form');
    const form_like = document.querySelector('#like-form');
    const form_fave = document.querySelector('#fave-form');

    // If forms are not null, listen to form submission event
    if (form_comment && form_like && form_fave) {
        const resource_id = document.querySelector('#resource-id').value;

        form_comment.onsubmit = () => add_comment(resource_id);
        form_like.onsubmit = () => update(resource_id, 'like');
        form_fave.onsubmit = () => update(resource_id, 'fave');
    }

    document.querySelectorAll('.del-comment-form').forEach(form => {
        form.onsubmit = () => delete_comment(form);
    });
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
        mode: 'same-origin', // Do not send CSRF token to another domain
        body: JSON.stringify({
            comment: element_comment.value
        })
    })
    .then(response => response.json())
    .then(result => {
        const element = document.createElement('div');
        element.classList.add('card', 'mb-3', 'comment');
        element.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${result['username']}</h5>
                <form class="del-comment-form float-end" data-cid="${result['cid']}" method="post">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                    <button class="btn-none" type="submit"><i class="fas fa-trash-alt"></i></button>
                </form>
                <p class="card-text">${element_comment.value}</p>
                <p class="card-text"><small class="text-muted">${result['timestamp']}</small></p>
            </div>
        `;
        document.querySelector('#comments').append(element);
        element_comment.value = '';

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

        // Update NodeList to include newly added comment
        document.querySelectorAll('.del-comment-form').forEach(form => {
            form.onsubmit = () => delete_comment(form);
        });
    })
    .catch(error => {
        console.log(error);
    });

    // Prevent default submission
    return false;
}

function delete_comment(element_form) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const resource_id = document.querySelector('#resource-id').value;
    const element_comment = element_form.parentElement.parentElement;

    fetch(`/resource/${resource_id}/comment`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            comment_id: element_form.dataset.cid
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result['error']) {
            console.log(result)
        } else {

            // Delete the comment
            element_comment.style.animationPlayState = 'running';
            element_comment.addEventListener('animationend', () => {
                element_comment.remove();
            });
        }
    })
    .catch(error => {
        console.log(error);
    });

    return false;
}

/**
 * Update resource's like or favorite field
 */
function update(resource_id, action) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/resource/${resource_id}/update`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            action: action
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result['error']) {
            console.log(result);
        } else {
            const element_icon = document.querySelector(`.${result['icon']}`);

            // Toggle between regular and solid icon
            if (element_icon.classList.contains('far')) {
                element_icon.classList.replace('far', 'fas');
            } else {
                element_icon.classList.replace('fas', 'far');
            }

            // Update number of like/favorite
            document.querySelector(`#${result['icon']}-count`).innerHTML = ` ${result['count']} `;
        }
    })
    .catch(error => {
        console.log(error);
    });

    return false;
}
