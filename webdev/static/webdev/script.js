document.addEventListener('DOMContentLoaded', function() {

    // Shortcut key
    onkeydown = event => {
        const search_input = document.querySelector('#search-input');

        // Select or deselect serach input
        if (event.ctrlKey && event.key === '/') {
            search_input.focus();
        } else if (event.key === 'Escape') {
            if (document.activeElement === search_input) {
                search_input.blur();
            }
        }
    }
});