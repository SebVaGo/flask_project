// Función para agregar un producto a la tabla de edición de la orden
function addProductToOrder(productId, productName, productPrice) {
    // Verificar si el producto ya existe en la tabla
    const existingRow = document.querySelector(`tr[data-producto-id="${productId}"]`);
    if (existingRow) {
      const quantityInput = existingRow.querySelector('.quantity-input');
      quantityInput.value = parseInt(quantityInput.value) + 1;
    } else {
      const tbody = document.getElementById('orderEditList');
      const row = document.createElement('tr');
      row.setAttribute('data-producto-id', productId);
      row.innerHTML = `
        <td>${productName}</td>
        <td>
          <input type="number" class="form-control form-control-sm quantity-input" value="1" min="1">
        </td>
        <td>
          <button type="button" class="btn btn-danger btn-sm" onclick="removeProductRow(this)">Eliminar</button>
        </td>
      `;
      tbody.appendChild(row);
    }
  }
  
  // Función para eliminar la fila correspondiente a un producto de la orden
  function removeProductRow(button) {
    const row = button.closest('tr');
    row.parentNode.removeChild(row);
  }
  
  // Obtiene el token CSRF del input hidden
  function getCsrfToken() {
    return document.querySelector("input[name='csrf_token']").value;
  }
  
  // Envía la data actualizada de la orden al backend
  function submitOrderUpdate(ordenId) {
    const rows = document.querySelectorAll("#orderEditList tr");
    let products = [];
    rows.forEach(row => {
      const productId = row.getAttribute("data-producto-id");
      const quantityInput = row.querySelector(".quantity-input");
      const quantity = parseInt(quantityInput.value);
      if (productId && quantity > 0) {
        products.push({ producto_id: productId, cantidad: quantity });
      }
    });
    
    const orderData = {
        // Ahora sí es un número entero
        usuario_id: window.USER_ID,
        products: products
      };
  
    fetch(`/orders/${ordenId}/edit`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken()
      },
      credentials: "same-origin",
      body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Se puede redireccionar o mostrar un mensaje de éxito
        alert("Orden actualizada exitosamente");
        window.location.href = "/orders";
      } else {
        alert("Error: " + data.message);
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Error inesperado al actualizar la orden");
    });
  }
  