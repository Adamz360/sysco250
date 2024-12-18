let selectedItems = [];
document.addEventListener('DOMContentLoaded', function () {
    const productSelect = document.getElementById('product');
    const categorySelect = document.getElementById('category');
    const quantityInput = document.getElementById('quantity');
    const addProductButton = document.getElementById('add-products');
    const selectedProductsTable = document.getElementById('selected-products-table').querySelector('tbody');

    addProductButton.addEventListener('click', function () {
        // Get values
        const selectedProduct = productSelect.options[productSelect.selectedIndex];
        const selectedCategory = categorySelect.options[categorySelect.selectedIndex];
        const quantity = parseInt(quantityInput.value);
        const unitPrice = parseFloat(selectedProduct.getAttribute('data-price'));
        const totalPrice = unitPrice * quantity;
        // Add a new row to the table
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${selectedProduct.text}</td>
            <td>${selectedCategory.text}</td>
            <td><input type="number" value="${quantity}" min="1" class="form-control quantity-input"></td>
            <td>N${unitPrice.toFixed(2)}</td>
            <td class="total-price">N${totalPrice.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-primary update-product">Update</button>
                <button class="btn btn-sm btn-danger delete-product">Delete</button>
            </td>
        `;
        selectedProductsTable.appendChild(row);

        // Clear inputs
        quantityInput.value = 1;
        productSelect.selectedIndex = 0;
        categorySelect.selectedIndex = 0;

        const newItem = {
            id:selectedProduct.value,
            description: selectedProduct.text,
            quantity: quantity,
            price: unitPrice,
            amount: totalPrice
        };
        selectedItems.push(newItem);
        updateSelectedItems(); // Update table and hidden input

    });


    categorySelect.addEventListener('change', function () {
        const categoryId = categorySelect.value;

        // Clear current product options
        productSelect.innerHTML = '<option selected disabled>Select Product</option>';

        // Fetch products by category using AJAX
        fetch(`/products-by-category/${categoryId}/`) // Replace with your backend endpoint
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                data.products.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.id;
                    console.log(option.value)
                    option.textContent = product.name;
                    option.setAttribute('data-price', product.price);
                    productSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    });


function updateSelectedItems() {
    const tableBody = document.getElementById('selected-products-table').querySelector('tbody');
    if (!Array.isArray(selectedItems) || selectedItems.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No items selected.</td></tr>';
        document.getElementById('items-Input').value = ''; // Clear hidden input
        return;
    }
    const fragment = document.createDocumentFragment();

    selectedItems.forEach((item, index) => {
        if (!item.description || !item.quantity || !item.price || !item.amount) {
            console.warn(`Invalid item at index ${index}`, item);
            return; // Skip invalid entries
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.description}</td>
            <td>${item.quantity}</td>
            <td>N${item.price.toFixed(2)}</td>
            <td>N${item.amount.toFixed(2)}</td>
            <td>
                <button class="btn btn-danger btn-sm remove-item" data-index="${index}">Remove</button>
            </td>
        `;
        fragment.appendChild(row);
    });

    tableBody.innerHTML = ''; // Clear current rows
    tableBody.appendChild(fragment);

    document.getElementById('items-Input').value = JSON.stringify(selectedItems);
}

document.getElementById('selected-products-table').querySelector('tbody').addEventListener('click', function (e) {
    const target = e.target;
    if (target.classList.contains('edit-items')) {
        const index = parseInt(target.getAttribute('data-index'));
        editItem(index);
    } else if (target.classList.contains('remove-item')) {
        const index = parseInt(target.getAttribute('data-index'));
        removeItem(index);
    }
});

function editItem(index) {
    if (index < 0 || index >= selectedItems.length) {
        alert("Invalid item selected for editing.");
        return;
    }
    const item = selectedItems[index];
    document.getElementById('product').value = item.description;
    document.getElementById('quantity').value = item.quantity;
    selectedItems.splice(index, 1);
    updateSelectedItems();
}


function removeItem(index) {
    if (index < 0 || index >= selectedItems.length) {
        alert("Invalid item selected for removal.");
        return;
    }
    selectedItems.splice(index, 1);
    updateSelectedItems();
}

document.getElementById('invoiceForm').addEventListener('submit', function (e) {
    // Ensure the items input has valid data
    const itemsInput = document.getElementById('items-Input');
    if (!itemsInput.value || itemsInput.value === '[]') {
        alert("Please add items to the invoice.");
        e.preventDefault();
        return;
    }

    // Prompt for payment method
    const paymentMethod = prompt("Enter Payment Method (e.g., Cash, POS, Bank Transfer):", "Cash");
    if (paymentMethod) {
        document.getElementById('paymentMethodInput').value = paymentMethod;
    } else {
        e.preventDefault(); // Prevent submission if no payment method is entered
    }
});



});

document.addEventListener('DOMContentLoaded', function () {
    const productSelect = document.getElementById('product');
    const availableQuantityText = document.getElementById('available-quantity');

    productSelect.addEventListener('change', function () {
        const productId = productSelect.value;

        if (!productId) {
            availableQuantityText.textContent = "Available quantity: --";
            return;
        }

        // Fetch available quantity for the selected product
        fetch(`/product-quantity/${productId}/`) // Replace with your backend endpoint
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch product quantity.');
                return response.json();
            })
            .then(data => {
                availableQuantityText.textContent = `Available quantity: ${data.available_quantity}`;
            })
            .catch(error => {
                console.error('Error fetching available quantity:', error);
                availableQuantityText.textContent = "Available quantity: Error fetching data.";
            });
    });
});