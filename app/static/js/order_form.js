// Array (o lista) que representa los productos en la orden
// En edición, se inicializa a partir de las filas en el DOM
let cart = [];

// Cuando cargue el DOM, sincronizamos la tabla con cart (si es edición)
document.addEventListener("DOMContentLoaded", function() {
  // Cargamos los productos iniciales si estamos en edición
  if (isEdit) {
    const rows = document.querySelectorAll("#orderEditList tr");
    rows.forEach(row => {
      const productId = row.getAttribute("data-producto-id");
      const quantity = parseInt(row.querySelector(".quantity-input").value);
      cart.push({ producto_id: productId, cantidad: quantity });
    });
  }
});

// Añade un producto a la lista "cart"
window.addProductToOrder = function(productId, productName) {
  // Ver si ya existe en cart
  let existing = cart.find(p => p.producto_id === productId);
  if (existing) {
    existing.cantidad++;
  } else {
    cart.push({ producto_id: productId, cantidad: 1 });
  }
  renderCart();
};

// Elimina la fila desde el botón "Eliminar"
window.removeProductRow = function(button) {
  const row = button.closest("tr");
  const productId = row.getAttribute("data-producto-id");
  // Eliminamos del DOM
  row.remove();
  // Quitamos del array cart
  cart = cart.filter(p => p.producto_id !== productId);
};

// Reconstruye la tabla #orderEditList en base a cart
function renderCart() {
  const tbody = document.getElementById("orderEditList");
  tbody.innerHTML = "";
  cart.forEach(item => {
    const row = document.createElement("tr");
    row.setAttribute("data-producto-id", item.producto_id);
    row.innerHTML = `
      <td>Producto #${item.producto_id}</td>
      <td>
        <input type="number" class="form-control form-control-sm quantity-input" 
               value="${item.cantidad}" min="1"
               onchange="updateQuantity('${item.producto_id}', this.value)">
      </td>
      <td>
        <button type="button" class="btn btn-danger btn-sm" onclick="removeProductRow(this)">Eliminar</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// Actualiza la cantidad en cart cuando se modifica el input
window.updateQuantity = function(productId, newValue) {
  let found = cart.find(p => p.producto_id === productId);
  if (found) {
    const qty = parseInt(newValue);
    if (qty > 0) {
      found.cantidad = qty;
    } else {
      // Si el usuario pone 0 o negativo, lo eliminamos
      cart = cart.filter(p => p.producto_id !== productId);
    }
    renderCart();
  }
};

// Obtiene el token CSRF del input hidden
function getCsrfToken() {
  return document.querySelector("input[name='csrf_token']").value;
}

// Envía la data de la orden (creación o edición) al backend
window.submitOrder = function() {
  // Si es edición => PUT /orders/<orderId>/edit
  // Si es creación => POST /orders
  let url, method;
  if (isEdit && orderId) {
    url = `/orders/${orderId}/edit`;
    method = "PUT";
  } else {
    url = "/orders";
    method = "POST";
  }

  // Recolectamos la info final de cart
  // (cart ya está sincronizado con la tabla)
  const orderData = {
    usuario_id: parseInt(userId),
    products: cart
  };

  fetch(url, {
    method: method,
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
      alert(isEdit ? "Orden actualizada con éxito" : "Orden creada con éxito");
      // Redirigimos a la lista de órdenes
      window.location.href = "/orders";
    } else {
      alert("Error: " + data.message);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error inesperado al procesar la orden");
  });
};
