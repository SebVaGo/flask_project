document.addEventListener("DOMContentLoaded", function () {
    let cart = [];

    function getCsrfToken() {
        return document.querySelector("input[name='csrf_token']").value;
    }

    window.addToCart = function(id, name, price) {
        let existingProduct = cart.find(p => p.id === id);
        if (existingProduct) {
            existingProduct.quantity++;
        } else {
            cart.push({ id, name, price, quantity: 1 });
        }
        updateCart();
    };

    function updateCart() {
        let orderList = document.getElementById("orderList");
        let orderTable = document.getElementById("orderTable");
        let buyButton = document.getElementById("buyButton");
        orderList.innerHTML = "";

        if (cart.length > 0) {
            orderTable.style.display = "table";
            buyButton.style.display = "block";
        } else {
            orderTable.style.display = "none";
            buyButton.style.display = "none";
        }

        cart.forEach((product, index) => {
            orderList.innerHTML += `
                <tr>
                    <td>${product.name}</td>
                    <td>
                        <input type="number" value="${product.quantity}" min="1"
                               class="form-control form-control-sm"
                               onchange="updateQuantity(${index}, this.value)">
                    </td>
                    <td>S/ ${(product.price * product.quantity).toFixed(2)}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="removeFromCart(${index})">Eliminar</button>
                    </td>
                </tr>`;
        });
    }

    window.updateQuantity = function(index, value) {
        let newQuantity = parseInt(value);
        if (newQuantity > 0) {
            cart[index].quantity = newQuantity;
            updateCart();
        }
    };

    window.removeFromCart = function(index) {
        cart.splice(index, 1);
        updateCart();
    };

    window.submitOrder = function() {
        if (cart.length === 0) {
            alert("No hay productos en la orden.");
            return;
        }

        let orderData = {
            usuario_id: 33, 
            products: cart.map(p => ({ producto_id: p.id, cantidad: p.quantity }))
        };

        fetch("/orders", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()  
            },
            credentials: "same-origin",
            body: JSON.stringify(orderData)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Orden creada con éxito.");
                cart = [];
                updateCart();
            } else {
                alert("Error al crear la orden: " + data.message);
            }
        })
        .catch(() => alert("Error inesperado al crear la orden."));
    };

    window.deleteProduct = function(productId) {
        if (!confirm("¿Seguro que deseas eliminar este producto?")) return;

        fetch(`/admin/products/${productId}/delete`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken() 
            },
            credentials: "same-origin"
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Producto eliminado correctamente.");
                location.reload();
            } else {
                alert("Error al eliminar el producto: " + data.message);
            }
        })
        .catch(error => {
            console.error(error);
            alert("Error inesperado al eliminar el producto.");
        });
    };
});
