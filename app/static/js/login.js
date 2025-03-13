document.addEventListener("DOMContentLoaded", function () {
    
    function getCsrfToken() {
        return document.querySelector("input[name='csrf_token']").value;  
    }

    window.submitLogin = function () {
        let form = document.getElementById("loginForm");
        let formData = new FormData(form);
        let messagesDiv = document.getElementById("messages");

        let url = form.getAttribute("data-url");  

        document.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
        document.querySelectorAll(".invalid-feedback").forEach(el => el.innerText = "");

        fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCsrfToken()  
            },
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.data.redirect_url;  
            } else {
                if (data.errors) {
                    for (let field in data.errors) {
                        let input = document.querySelector(`[name="${field}"]`);
                        let errorDiv = document.getElementById(`error-${field}`);
                        if (input) {
                            input.classList.add("is-invalid");
                        }
                        if (errorDiv) {
                            errorDiv.innerText = data.errors[field][0];  
                        }
                    }
                } else {
                    messagesDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
                }
            }
        })
        .catch(error => {
            console.error("Error:", error);
            messagesDiv.innerHTML = `<div class="alert alert-danger">Error interno del servidor.</div>`;
        });
    };
});
