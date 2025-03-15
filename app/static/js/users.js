document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".delete-user");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            const userId = this.getAttribute("data-id");
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;

            if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
                fetch(`/users/${userId}/delete`, {
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": csrfToken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Usuario eliminado correctamente.");
                        location.reload();
                    } else {
                        alert("Error: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("Hubo un problema al intentar eliminar el usuario.");
                });
            }
        });
    });
});
