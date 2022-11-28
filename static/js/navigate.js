document.addEventListener('DOMContentLoaded', function() {
    const nav_list = document.getElementsByClassName('list-group-item-action');
    const page_title = document.getElementById('page_title');

    for (const element of nav_list) {
        if (element.innerText === page_title.value) {
            element.classList.add('list-group-item-secondary');
            element.classList.add('active');
            break;
        }
    }
});