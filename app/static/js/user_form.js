document.addEventListener("DOMContentLoaded", () => {
  window.submitUserForm = function () {
    const form = document.getElementById("userForm");
    const formData = new FormData(form);
    const messagesDiv = document.getElementById("messages");

    document.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
    document.querySelectorAll(".invalid-feedback").forEach(el => el.innerText = "");
      
    const csrfToken = formData.get("csrf_token");
    const url = form.getAttribute("data-url");
    const redirectUrl = form.getAttribute("data-redirect");

    fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken
      }
    })
    .then(response => response.json())
    .then(data => {
      messagesDiv.innerHTML = "";
      if (data.success) {
        messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
        if (redirectUrl) {
          setTimeout(() => { window.location.href = redirectUrl; }, 500);
        } else {
          form.reset();
        }
      } else {
        if (!data.errors) {
          messagesDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
        if (data.errors) {
          Object.keys(data.errors).forEach(field => {
            const input = document.querySelector(`[name="${field}"]`);
            if (input) {
              input.classList.add("is-invalid");
              input.nextElementSibling.innerText = data.errors[field].join(", ");
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

  document.querySelectorAll("#userForm input, #userForm select").forEach(input => {
    input.addEventListener("input", function () {
      if (this.classList.contains("is-invalid")) {
        this.classList.remove("is-invalid");
        this.nextElementSibling.innerText = "";
      }
    });
  });
});
