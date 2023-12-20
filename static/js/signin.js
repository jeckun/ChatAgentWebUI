function signIn(event) {
    event.preventDefault();

    // Get values from the form
    var username = document.getElementById('inputUsername').value;
    var email = document.getElementById('inputEmail').value;
    var password = document.getElementById('inputPassword').value;

    console.log('signIn:', username, email, password)

    // Perform the login logic with server communication
    fetch('/signin', {
        method: 'POST',
        body: new URLSearchParams({username, email, password }), // Send data as form data
    })
    .then(response => response.json())
    .then(data => {
        console.log('Login response:', data);
    })
    .catch(error => {
        console.error('Error during login:', error);
    });
}


function signUp() {
    // Get values from the form
    var username = document.getElementById('inputUsername').value;
    var email = document.getElementById('inputEmail').value;
    var password = document.getElementById('inputPassword').value;

    console.log('signUp:', username, email, password)

    // Perform the registration logic with server communication
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Registration response:', data);
    })
    .catch(error => {
        console.error('Error during registration:', error);
    });
}