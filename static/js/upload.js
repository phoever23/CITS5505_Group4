const categorySubcategories = {
  Housing: ["Rent", "Mortgage", "Utilities", "Home Insurance", "Maintenance"],
  Food: ["Groceries", "Restaurants", "Takeout", "Coffee Shops", "Alcohol"],
  Shopping: ["Clothing", "Electronics", "Furniture", "Books", "Gifts"],
  Education: ["Tuition", "Textbooks", "Supplies", "Printing", "Courses"],
  Others: ["Transportation", "Healthcare", "Entertainment", "Travel", "Gym"],
};

async function sendData(formData) {
  try {
    const response = await fetch("/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    const result = await response.json();
    if (response.ok) {
      showNotification("Expenses added successfully", "success");
    } else {
      const errorMessage = result.message || "Failed to add expense";
      showNotification(errorMessage, "error");
    }
  } catch (e) {
    console.error(e);
    showNotification("Network error occurred", "error");
  }
}

async function sendFile(formData) {
  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log(result);
    if (response.ok) {
      showNotification("CSV file uploaded successfully", "success");
    } else {
      const errorMessage = result.message || "CSV upload failed";
      showNotification("Network error while uploading CSV", "error");
    }
  } catch (e) {
    console.error(e);
  }
}

function showNotification(message, type) {
  Toastify({
    text: message,
    className: type,
    duration: 3000,
  }).showToast();
}

document.addEventListener("DOMContentLoaded", function () {
  const categorySelect = document.getElementById("entryCategory");
  const subcategorySelect = document.getElementById("entrySubcategory");
  const manualEntryForm = document.getElementById("manualEntryForm");
  const fileEntryForm = document.getElementById("fileEntryForm");
  const csvUploadInput = document.getElementById("csvUpload");
  const processCsvBtn = document.querySelector(".upload-btn");
  categorySelect.addEventListener("change", function () {
    const selectedCategory = this.value;
    subcategorySelect.innerHTML =
      '<option value="">Select Sub-category</option>';

    if (selectedCategory && categorySubcategories[selectedCategory]) {
      categorySubcategories[selectedCategory].forEach(function (subcategory) {
        const option = document.createElement("option");
        option.value = subcategory;
        option.textContent = subcategory;
        subcategorySelect.appendChild(option);
      });
    }
  });
  manualEntryForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = {
      date: document.getElementById("entryDate").value,
      category: categorySelect.value,
      subcategory: subcategorySelect.value,
      amount: document.getElementById("entryAmount").value,
      currency: document.getElementById("entryCurrency").value,
    };
    sendData(formData);
    this.reset();
  });

  fileEntryForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const file = csvUploadInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    sendFile(formData);
    this.reset();
  });
});
