const content_type = {
    book: {
        full: 'book',
        view: 'learn'
    },
    code: {
        full: 'code',
        view: 'practice'
    },
    crs: {
        full: 'course',
        view: 'learn'
    },
    doc: {
        full: 'document',
        view: 'learn'
    },
    fav: {
        full: 'favorite',
        view: 'user'
    },
    pub: {
        full: 'published',
        view: 'user'
    },
    quiz: {
        full: 'quiz',
        view: 'practice'
    },
    vid: {
        full: 'video',
        view: 'learn'
    }
};

const level = {
    INTR: {
        full: 'Introductory',
        color: 'text-success'
    },
    MEDI: {
        full: 'Intermediate',
        color: 'text-warning'
    },
    ADVC: {
        full: 'Advanced',
        color: 'text-danger'
    }
};

document.addEventListener('DOMContentLoaded', function() {

    // Use nav-tab to toggle between contents
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.onclick = () => {
            history.pushState({content: content_type[tab.dataset.content]}, '', content_type[tab.dataset.content]['full']);
            load_content(content_type[tab.dataset.content]);
        }
    });
});

window.onpopstate = (event) => {
    if (event.state) {
        load_content(event.state.content);
    } else {
        window.history.go(0);
    }
}

function load_content(content_type) {
    if (content_type['view'] === 'learn') {
        const element_book = document.querySelector('#tab-book');
        const element_crs = document.querySelector('#tab-course');
        const element_doc = document.querySelector('#tab-document');
        const element_vid = document.querySelector('#tab-video');
    
        // Remove .active class (if any)
        if (element_book.classList.contains('active')) {
            element_book.classList.remove('active');
        }
        if (element_crs.classList.contains('active')) {
            element_crs.classList.remove('active');
        }
        if (element_doc.classList.contains('active')) {
            element_doc.classList.remove('active');
        }
        if (element_vid.classList.contains('active')) {
            element_vid.classList.remove('active');
        }
    } else if (content_type['view'] === 'practice') {
        const element_code = document.querySelector('#tab-code');
        const element_quiz = document.querySelector('#tab-quiz');

        if (element_code.classList.contains('active')) {
            element_code.classList.remove('active');
        }
        if (element_quiz.classList.contains('active')) {
            element_quiz.classList.remove('active');
        }
    } else {
        const element_fav = document.querySelector('#tab-favorite');
        const element_pub = document.querySelector('#tab-published');

        if (element_fav.classList.contains('active')) {
            element_fav.classList.remove('active');
        }
        if (element_pub.classList.contains('active')) {
            element_pub.classList.remove('active');
        }
    }

    // Add .active class to selected content type
    document.querySelector(`#tab-${content_type['full']}`).classList.add('active');

    const element_content = document.querySelector('#content');
    element_content.innerHTML = '';

    fetch(`/getcontent/${content_type['full']}`)
    .then(response => response.json())
    .then(resources => {
        if (resources['error']) {
            element_content.innerHTML = `<h2>${resources['error']}</h2>`;
        } else {
            resources.forEach(resource => {
                const element = document.createElement('div');
                element.classList.add('card', 'mb-4');
                element.innerHTML = `
                    <a class="text-body text-decoration-none" href="/resource/${resource.id}">
                        <div class="card-header">${resource.language}</div>
                        <div class="card-body">
                            <h5 class="card-title">${resource.title}</h5>
                            <p class="card-text">${resource.description}</p>
                            <p class="card-text">Level: <span class="${level[resource.level]['color']}">${level[resource.level]['full']}</span></p>
                        </div>
                        <div class="card-footer"><small class="text-muted">${resource.timestamp}</small></div>
                    </a>
                `;
                element_content.append(element);
            });
        }
    })
    .catch(error => {
        console.log(error);
    });
}
