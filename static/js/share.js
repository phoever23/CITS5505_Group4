// Data type selection handler
document.getElementById("dataType").addEventListener("change", function () {
  const categorySection = document.getElementById("categorySection");
  if (this.value === "summary") {
    categorySection.style.display = "block";
  } else {
    categorySection.style.display = "none";
  }
});

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
  const dataType = document.getElementById("dataType").value;
  const dateRange = document.getElementById("dateRange").value;
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  const categories = Array.from(
    document.getElementById("categoriesToShare").selectedOptions
  ).map((opt) => opt.value);
  const shareWith = document.getElementById("shareWith").value;

  const shareData = {
    dataType,
    dateRange,
    startDate: dateRange === "custom" ? startDate : null,
    endDate: dateRange === "custom" ? endDate : null,
    categories: dataType === "summary" ? categories : [],
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
