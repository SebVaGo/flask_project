document.addEventListener("DOMContentLoaded", function () {
    
    function getCsrfToken() {
        return document.querySelector("input[name='csrf_token']").value;
    }

    window.updateQuantity = function(orderId, productId, newQuantity) {
        fetch(`/orders/${orderId}/${productId}/update`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken() 
            },
            body: JSON.stringify({ cantidad: parseInt(newQuantity) }),
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Error: " + data.message);
            } else {
                location.reload();
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Hubo un error inesperado.");
        });
    };

    window.deleteProduct = function(orderId, productId) {
        if (!confirm("¿Seguro que deseas eliminar este producto de la orden?")) return;

        fetch(`/orders/${orderId}/${productId}/delete`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()
            },
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Error al eliminar el producto: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    };
});
