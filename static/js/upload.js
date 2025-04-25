// Define the category to subcategory mapping
const categorySubcategories = {
    housing: ["Rent", "Mortgage", "Utilities", "Home Insurance", "Maintenance"],
    food: ["Groceries", "Restaurants", "Takeout", "Coffee Shops", "Alcohol"],
    shopping: ["Clothing", "Electronics", "Furniture", "Books", "Gifts"],
    education: ["Tuition", "Textbooks", "Supplies", "Printing", "Courses"],
    others: ["Transportation", "Healthcare", "Entertainment", "Travel", "Gym"]
};

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const categorySelect = document.getElementById('entryCategory');
    const subcategorySelect = document.getElementById('entrySubcategory');
    const manualEntryForm = document.getElementById('manualEntryForm');
    const csvUploadInput = document.getElementById('csvUpload');
    const processCsvBtn = document.querySelector('.upload-btn');
    
    // Populate subcategories based on category selection
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
    
    // Handle manual form submission
    manualEntryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const formData = {
            date: document.getElementById('entryDate').value,
            category: categorySelect.value,
            subcategory: subcategorySelect.value,
            amount: document.getElementById('entryAmount').value,
            currency: document.getElementById('entryCurrency').value
        };
        
        // Here you would typically send this data to your backend
        console.log('Form submitted:', formData);
        
        // Show success message
        alert('Expense added successfully!');
        
        // Reset form
        this.reset();
    });
    
    // Handle CSV file processing
    processCsvBtn.addEventListener('click', function() {
        const file = csvUploadInput.files[0];
        
        if (!file) {
            alert('Please select a CSV file first.');
            return;
        }
        
        // Process the CSV file (you would add your CSV parsing logic here)
        console.log('Processing CSV file:', file.name);
        
        // Example using FileReader
        const reader = new FileReader();
        reader.onload = function(e) {
            const contents = e.target.result;
            // Parse CSV content (you might want to use a library like PapaParse)
            console.log('CSV content:', contents);
            alert('CSV file processed successfully!');
        };
        reader.readAsText(file);
    });
});