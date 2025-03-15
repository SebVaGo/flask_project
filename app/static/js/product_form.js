document.addEventListener("DOMContentLoaded", function () {
    window.submitProduct = function () {
      const form = document.getElementById("productForm");
      const formData = new FormData(form);
      const messagesDiv = document.getElementById("messages");
  
      document.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
      document.querySelectorAll(".invalid-feedback").forEach(el => el.innerText = "");
  
      const url = form.getAttribute("data-url");
      const redirectUrl = form.getAttribute("data-redirect");
      const csrfToken = form.querySelector("input[name='csrf_token']").value;
  
      fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrfToken },
        credentials: "same-origin"
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
          setTimeout(() => { window.location.href = redirectUrl; }, 500);
        } else {
          if (!data.errors) {
            messagesDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
          }
          if (data.errors) {
            Object.keys(data.errors).forEach(field => {
              const input = document.querySelector(`[name="${field}"]`);
              const errorDiv = document.getElementById(`error-${field}`);
              if (input) {
                input.classList.add("is-invalid");
              }
              if (errorDiv) {
                errorDiv.innerText = data.errors[field].join(", ");
              }
            });
          }
        }
      })
      .catch(error => {
        console.error("Error:", error);
        messagesDiv.innerHTML = `<div class="alert alert-danger">Error interno del servidor.</div>`;
      });
    };
  });
  