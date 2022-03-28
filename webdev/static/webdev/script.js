const content_type = {
    book: ['BOOK', 'book'],
    code: ['CODE', 'code'],
    crs: ['CRS', 'course'],
    doc: ['DOC', 'document'],
    fav: ['FAV', 'favorite'],
    pub: ['PUB', 'published'],
    quiz: ['QUIZ', 'quiz'],
    vid: ['VID', 'video']
};

document.addEventListener('DOMContentLoaded', function() {

    // Use dropdown to toggle between views
    document.getElementById('dropdown-favorite').onclick = () => {
        load_view('user');
        load_content(content_type['fav']);
    }
    document.getElementById('dropdown-published').onclick = () => {
        load_view('user');
        load_content(content_type['pub']);
    }
    document.getElementById('dropdown-book').onclick = () => {
        load_view('learn');
        load_content(content_type['book']);
    }
    document.getElementById('dropdown-course').onclick = () => {
        load_view('learn');
        load_content(content_type['crs']);
    }
    document.getElementById('dropdown-document').onclick = () => {
        load_view('learn');
        load_content(content_type['doc']);
    }
    document.getElementById('dropdown-video').onclick = () => {
        load_view('learn');
        load_content(content_type['vid']);
    }
    document.getElementById('dropdown-code').onclick = () => {
        load_view('practice');
        load_content(content_type['code']);
    }
    document.getElementById('dropdown-quiz').onclick = () => {
        load_view('practice');
        load_content(content_type['quiz']);
    }

    // Use nav-tab to toggle between contents
    document.getElementById('tab-favorite').onclick = () => load_content(content_type['fav']);
    document.getElementById('tab-published').onclick = () => load_content(content_type['pub']);
    document.getElementById('tab-book').onclick = () => load_content(content_type['book']);
    document.getElementById('tab-course').onclick = () => load_content(content_type['crs']);
    document.getElementById('tab-document').onclick = () => load_content(content_type['doc']);
    document.getElementById('tab-video').onclick = () => load_content(content_type['vid']);
    document.getElementById('tab-code').onclick = () => load_content(content_type['code']);
    document.getElementById('tab-quiz').onclick = () => load_content(content_type['quiz']);
});

function load_content(content_type) {
    let view = '';

    if (document.getElementById('learn-view').style.display === 'block') {
        view = 'learn';
        const element_book = document.getElementById('tab-book');
        const element_crs = document.getElementById('tab-course');
        const element_doc = document.getElementById('tab-document');
        const element_vid = document.getElementById('tab-video');
    
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
    } else if (document.getElementById('practice-view').style.display === 'block') {
        view = 'practice';
        const element_code = document.getElementById('tab-code');
        const element_quiz = document.getElementById('tab-quiz');

        if (element_code.classList.contains('active')) {
            element_code.classList.remove('active');
        }
        if (element_quiz.classList.contains('active')) {
            element_quiz.classList.remove('active');
        }
    } else if (document.getElementById('user-view').style.display === 'block') {
        view = 'user';
        const element_fav = document.getElementById('tab-favorite');
        const element_pub = document.getElementById('tab-published');

        if (element_fav.classList.contains('active')) {
            element_fav.classList.remove('active');
        }
        if (element_pub.classList.contains('active')) {
            element_pub.classList.remove('active');
        }
    }
    // Add .active class to selected content type
    document.getElementById(`tab-${content_type[1]}`).classList.add('active');

    fetch(`/resource/${content_type[0]}`)
    .then(response => response.json())
    .then(resources => {
        if (resources['error']) {
            console.log(resources);
        } else {
            resources.forEach(resource => {
                const element = document.createElement('div');
                element.classList.add('card', 'mb-3');
                element.innerHTML = `
                    <a class="text-body text-decoration-none" href="/resource/${resource.id}">
                        <div class="card-header">TODO</div>
                        <div class="card-body">
                            <h5 class="card-title">${resource.title}</h5>
                            <p class="card-text">${resource.description}</p>
                            <p class="card-text"><small class="text-muted">${resource.timestamp}</small></p>
                        </div>
                        <div class="card-footer>Level: TODO</div>
                    </a>
                `;
                document.getElementById(`${view}-view`).append(element);
            });
        }
    })
    .catch(error => {
        console.log(error);
    });
}

function load_view(view) {

    // Show selected view and hide other views
    document.getElementById('home-view').style.display = 'none';
    document.getElementById('learn-view').style.display = 'none';
    document.getElementById('practice-view').style.display = 'none';
    document.getElementById('user-view').style.display = 'none';
    document.getElementById(`${view}-view`).style.display = 'block';
}
