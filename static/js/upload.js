const categorySubcategories = {
    housing: ["Rent", "Mortgage", "Utilities", "Home Insurance", "Maintenance"],
    food: ["Groceries", "Restaurants", "Takeout", "Coffee Shops", "Alcohol"],
    shopping: ["Clothing", "Electronics", "Furniture", "Books", "Gifts"],
    education: ["Tuition", "Textbooks", "Supplies", "Printing", "Courses"],
    others: ["Transportation", "Healthcare", "Entertainment", "Travel", "Gym"]
};

async function sendData(formData) {
    console.log('called') 
    try {
        const response = await fetch("/upload", {
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(formData),
        });
        console.log(await response);
    } catch (e) {
        console.error(e);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('entryCategory');
    const subcategorySelect = document.getElementById('entrySubcategory');
    const manualEntryForm = document.getElementById('manualEntryForm');
    const csvUploadInput = document.getElementById('csvUpload');
    const processCsvBtn = document.querySelector('.upload-btn');
    categorySelect.addEventListener('change', function() {
        const selectedCategory = this.value;
        subcategorySelect.innerHTML = '<option value="">Select Sub-category</option>';
        
        if (selectedCategory && categorySubcategories[selectedCategory]) {
            categorySubcategories[selectedCategory].forEach(function(subcategory) {
                const option = document.createElement('option');
                option.value = subcategory.toLowerCase().replace(' ', '-');
                option.textContent = subcategory;
                subcategorySelect.appendChild(option);
            });
        }
    });
    manualEntryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = {
            date: document.getElementById('entryDate').value,
            category: categorySelect.value,
            subcategory: subcategorySelect.value,
            amount: document.getElementById('entryAmount').value,
            currency: document.getElementById('entryCurrency').value
        };
        sendData(formData);
        console.log('Form submitted:', formData);
        //alert('Expense added successfully!');
        this.reset();
    });
});