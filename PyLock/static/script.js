document.addEventListener('DOMContentLoaded', function() {
    const addPasswordForm = document.getElementById('add-password-form');
    const editPasswordForm = document.getElementById('edit-password-form');
    const deletePasswordForm = document.getElementById('delete-password-form');
    const searchPasswordsForm = document.getElementById('search-passwords-form');
    const passwordsList = document.getElementById('passwords-list');
    const searchResults = document.getElementById('search-results');

    addPasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(addPasswordForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
            website: formData.get('website')
        };
        fetch('/add_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            addPasswordForm.reset();
            loadPasswords();
        });
    });

    editPasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(editPasswordForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
            website: formData.get('website')
        };
        const id = formData.get('id');
        fetch(`/edit_password/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            editPasswordForm.reset();
            loadPasswords();
        });
    });

    deletePasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(deletePasswordForm);
        const id = formData.get('id');
        fetch(`/delete_password/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            deletePasswordForm.reset();
            loadPasswords();
        });
    });

    searchPasswordsForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(searchPasswordsForm);
        const query = formData.get('query');
        fetch(`/search_passwords?query=${query}`)
        .then(response => response.json())
        .then(data => {
            searchResults.innerHTML = '';
            data.passwords.forEach(password => {
                const div = document.createElement('div');
                div.textContent = `Username: ${password.username}, Password: ${password.password}, Website: ${password.website}`;
                searchResults.appendChild(div);
            });
        });
    });

    function loadPasswords() {
        fetch('/view_passwords')
        .then(response => response.json())
        .then(data => {
            passwordsList.innerHTML = '';
            data.passwords.forEach(password => {
                const div = document.createElement('div');
                div.textContent = `Username: ${password.username}, Password: ${password.password}, Website: ${password.website}`;
                passwordsList.appendChild(div);
            });
        });
    }

    loadPasswords();
});
