document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const loginButton = document.getElementById("loginButton");

    loginButton.addEventListener("click", function(event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/dashboard";
            } else {
                alert("Login failed: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred during login.");
        });
    });
});