document.addEventListener("DOMContentLoaded", function () {
    
    function getCsrfToken() {
        return document.querySelector("input[name='csrf_token']").value;
    }
    
    window.deleteOrder = function(orderId) {
        if (!confirm("¿Seguro que deseas eliminar esta orden?")) return;

        fetch(`/orders/${orderId}/delete`, {
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
                location.href = "/orders";
            } else {
                alert("Error al eliminar la orden: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    }
});
