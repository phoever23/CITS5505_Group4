// Date range handler
document.getElementById("dateRange").addEventListener("change", function () {
  const customDateSection = document.getElementById("customDateSection");
  if (this.value === "custom") {
    customDateSection.style.display = "block";
  } else {
    customDateSection.style.display = "none";
  }
});

// User search functionality
let searchTimeout;
document.getElementById("shareWith").addEventListener("input", function () {
  clearTimeout(searchTimeout);
  const searchTerm = this.value.trim();

  if (searchTerm.length < 2) {
    document.getElementById("searchResults").style.display = "none";
    return;
  }

  searchTimeout = setTimeout(() => {
    fetch(`/api/search-users?term=${encodeURIComponent(searchTerm)}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const resultsContainer = document.getElementById("searchResults");
        resultsContainer.innerHTML = "";

        if (data.users && data.users.length > 0) {
          data.users.forEach((user) => {
            const div = document.createElement("div");
            div.className = "search-result-item";
            div.textContent = user.username;
            div.onclick = () => {
              document.getElementById("shareWith").value = user.username;
              resultsContainer.style.display = "none";
            };
            resultsContainer.appendChild(div);
          });
          resultsContainer.style.display = "block";
        } else {
          resultsContainer.innerHTML =
            "<div class='search-result-item'>No users found</div>";
          resultsContainer.style.display = "block";
        }
      })
      .catch((error) => {
        const resultsContainer = document.getElementById("searchResults");
        resultsContainer.innerHTML =
          "<div class='search-result-item error'>Error searching users. Please try again.</div>";
        resultsContainer.style.display = "block";
      });
  }, 300);
});

// Share button handler
document.getElementById("shareDataBtn").addEventListener("click", function () {
  const dateRange = document.getElementById("dateRange").value;
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const shareWith = document.getElementById("shareWith").value;

  const shareData = {
    dateRange,
    startDate: dateRange === "custom" ? startDate : null,
    endDate: dateRange === "custom" ? endDate : null,
    shareWith,
  };

  fetch("/api/share-data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(shareData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        document.getElementById("shareResult").innerHTML =
          '<div class="success-message">Data shared successfully!</div>';
      } else {
        document.getElementById(
          "shareResult"
        ).innerHTML = `<div class="error-message">${data.message}</div>`;
      }
    })
    .catch((error) => {
      document.getElementById("shareResult").innerHTML =
        '<div class="error-message">Error sharing data. Please try again.</div>';
    });
});

// Add these variables at the top
let currentPage = 1;

// Function to format date range for display
function formatDateRange(startDate, endDate) {
  if (!startDate && !endDate) return "All Time";

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  if (startDate && endDate) {
    return `${formatDate(startDate)} to ${formatDate(endDate)}`;
  } else if (startDate) {
    return `From ${formatDate(startDate)}`;
  } else if (endDate) {
    return `Until ${formatDate(endDate)}`;
  }
}

// Function to load shared data with pagination
function loadSharedData(page = 1) {
  currentPage = page;
  fetch(`/api/shared-expenses?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      const sharedDataList = document.getElementById("sharedDataList");
      sharedDataList.innerHTML = "";

      if (data.shared_data.length === 0) {
        sharedDataList.innerHTML =
          '<p class="text-gray-500">No shared data available.</p>';
        document.getElementById("pagination").style.display = "none";
        return;
      }

      data.shared_data.forEach((sharedData) => {
        const timestamp = sharedData.shared_at.split(" ");
        const [date, time] = timestamp;
        const div = document.createElement("div");
        div.className = "shared-data-item";
        div.innerHTML = `
                    <div class="shared-data-info">
                        <h3 class="font-semibold">Shared by ${
                          sharedData.shared_by
                        }</h3>
                        <p class="text-sm text-gray-600">Shared on ${
                          date + " " + time.slice(0, 5)
                        }</p>
                        <div class="shared-data-details mt-2">
                            <p class="text-sm">
                                <span class="font-medium">Date Range:</span> 
                                ${formatDateRange(
                                  sharedData.start_date,
                                  sharedData.end_date
                                )}
                            </p>
                        </div>
                    </div>
                    <div class="shared-data-actions">
                        <button class="view-shared-data-btn cta-btn"
                                data-expenses='${JSON.stringify(
                                  sharedData.expenses
                                )}'>
                            View Data
                        </button>
                    </div>
                `;
        sharedDataList.appendChild(div);
      });

      // Add event listeners to view buttons
      document.querySelectorAll(".view-shared-data-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
          const expenses = JSON.parse(this.dataset.expenses);
          // Store the expenses in localStorage
          localStorage.setItem("sharedExpenses", JSON.stringify(expenses));
          // Navigate to dashboard with shared view parameter
          window.location.href = "/dashboard?view=shared";
        });
      });

      // Update pagination
      updatePagination(data.pagination);
    })
    .catch((error) => {
      console.error("Error loading shared data:", error);
    });
}

// Function to update pagination controls
function updatePagination(pagination) {
  const paginationContainer = document.getElementById("pagination");
  paginationContainer.innerHTML = "";

  if (pagination.total_pages <= 1) {
    paginationContainer.style.display = "none";
    return;
  }

  paginationContainer.style.display = "flex";

  // Previous button
  const prevButton = document.createElement("button");
  prevButton.textContent = "Previous";
  prevButton.disabled = !pagination.has_prev;
  prevButton.onclick = () => loadSharedData(currentPage - 1);
  paginationContainer.appendChild(prevButton);

  // Page numbers
  for (let i = 1; i <= pagination.total_pages; i++) {
    const pageButton = document.createElement("button");
    pageButton.textContent = i;
    pageButton.className = i === pagination.current_page ? "active" : "";
    pageButton.onclick = () => loadSharedData(i);
    paginationContainer.appendChild(pageButton);
  }

  // Next button
  const nextButton = document.createElement("button");
  nextButton.textContent = "Next";
  nextButton.disabled = !pagination.has_next;
  nextButton.onclick = () => loadSharedData(currentPage + 1);
  paginationContainer.appendChild(nextButton);
}

// Load shared data when the page loads
document.addEventListener("DOMContentLoaded", function () {
  loadSharedData();
});
