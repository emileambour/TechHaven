document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const loginContainer = document.querySelector(".login-container");
    const registerContainer = document.getElementById("registerContainer");
    const showRegister = document.getElementById("showRegister");
    const showLogin = document.getElementById("showLogin");

    // Switch to Sign-up Form
    showRegister.addEventListener("click", function(event) {
        event.preventDefault();
        loginContainer.style.display = "none";
        registerContainer.style.display = "block";
    });

    // Switch back to Login Form
    showLogin.addEventListener("click", function(event) {
        event.preventDefault();
        registerContainer.style.display = "none";
        loginContainer.style.display = "block";
    });

    // User storage (mock database in localStorage)
    let users = JSON.parse(localStorage.getItem("users")) || {};

    // Login form submission
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;
        let errorMessage = document.getElementById("errorMessage");

        if (users[username] && users[username] === password) {
            localStorage.setItem("loggedInUser", username);
            window.location.href = "/home-page/home-page.html"; // Redirect on success
        } else {
            errorMessage.textContent = "Invalid username or password!";
        }
    });

    // Registration form submission with password validation
    registerForm.addEventListener("submit", function(event) {
        event.preventDefault();
        let newUsername = document.getElementById("newUsername").value;
        let newPassword = document.getElementById("newPassword").value;
        let registerMessage = document.getElementById("registerMessage");

        // Password validation: Must contain at least one letter and one number
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{6,}$/;

        if (users[newUsername]) {
            registerMessage.textContent = "Username already exists!";
            registerMessage.style.color = "red";
        } else if (!passwordRegex.test(newPassword)) {
            registerMessage.textContent = "Password must contain at least one letter and one number and be at least 6 characters long.";
            registerMessage.style.color = "red";
        } else {
            users[newUsername] = newPassword;
            localStorage.setItem("users", JSON.stringify(users));
            registerMessage.textContent = "Registration successful! You can now log in.";
            registerMessage.style.color = "green";
            setTimeout(() => {
                registerContainer.style.display = "none";
                loginContainer.style.display = "block";
            }, 1500);
        }
    });
});
