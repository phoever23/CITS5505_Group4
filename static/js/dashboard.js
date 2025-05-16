let originalData = [];
let currentFilter = "monthly";
let currentCurrency = "USD";
const budgetTarget = 2000;
let currentView = "personal"; // 'personal' or 'shared'
let currentSharedData = null;

const allowedCategories = {
  Housing: ["Rent", "Mortgage", "Utilities", "Home Insurance", "Maintenance"],
  Food: ["Groceries", "Restaurants", "Takeout", "Coffee Shops", "Alcohol"],
  Shopping: ["Clothing", "Electronics", "Furniture", "Books", "Gifts"],
  Education: ["Tuition", "Textbooks", "Supplies", "Printing", "Courses"],
  Others: ["Transportation", "Healthcare", "Entertainment", "Travel", "Gym"],
};

const allowedCurrencies = ["AUD", "GBP", "USD", "CAD", "EUR"];

// Events

document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    currentFilter = this.dataset.filter;
    drawCharts(originalData);
  });
});

document
  .getElementById("currencySelector")
  .addEventListener("change", function () {
    currentCurrency = this.value;
    drawCharts(originalData);
  });

document.getElementById("exportPNG").addEventListener("click", function () {
  exportCharts("png");
});

document.getElementById("exportPDF").addEventListener("click", function () {
  exportCharts("pdf");
});

// Charts

function drawCharts(data) {
  if (!data.length) return;

  const rates = { USD: 1, EUR: 0.9, INR: 83, AUD: 1.5, GBP: 0.8, CAD: 1.3 };
  const convert = (amt, cur) => (amt / rates[cur]) * rates[currentCurrency];

  const convertedBudgetTarget = convert(budgetTarget, "USD"); // Assuming budgetTarget is in USD

  const byPeriod = {},
    byCategory = {},
    bySubCategory = {};
  let totalExpense = 0,
    days = new Set();
  const sortedExpenses = data.sort((a, b) => b.amount - a.amount);

  data.forEach((entry) => {
    let period;
    if (currentFilter === "weekly") period = entry.date.slice(0, 7) + "-W";
    else if (currentFilter === "monthly") period = entry.date.slice(0, 7);
    else period = entry.date.slice(0, 4);

    const amt = convert(entry.amount, entry.currency);
    days.add(entry.date);

    byPeriod[period] = (byPeriod[period] || 0) + amt;
    byCategory[entry.category] = (byCategory[entry.category] || 0) + amt;
    bySubCategory[entry.subCategory] =
      (bySubCategory[entry.subCategory] || 0) + amt;
    totalExpense += amt;
  });

  document.getElementById("dailySpend").innerText = `${currentCurrency} ${(
    totalExpense / days.size
  ).toFixed(2)}`;

  const periods = Object.keys(byPeriod).sort();
  const expenses = periods.map((p) => byPeriod[p]);

  // Prediction
  const last3 = expenses.slice(-3);
  const avgLast3 = last3.reduce((a, b) => a + b, 0) / last3.length;
  const futurePeriods = predictNextPeriods(periods[periods.length - 1], 3);
  const futureData = Array(3).fill(avgLast3);

  destroyChart("lineChart");
  destroyChart("pieChart");
  destroyChart("barChart");

  // Line Chart
  new Chart(document.getElementById("lineChart"), {
    type: "line",
    data: {
      labels: [...periods, ...futurePeriods],
      datasets: [
        {
          label: `Expenses (${currentCurrency})`,
          data: expenses,
          borderColor: "orange",
          backgroundColor: "rgba(255,165,0,0.2)",
          tension: 0.3,
          fill: true,
        },
        {
          label: "Predicted Expenses",
          data: [...Array(periods.length).fill(null), ...futureData],
          borderColor: "red",
          borderDash: [5, 5],
          fill: false,
          tension: 0.3,
        },
        {
          label: "Budget Target",
          data: Array(periods.length + 3).fill(convertedBudgetTarget),
          borderColor: "green",
          borderDash: [10, 5],
          fill: false,
        },
      ],
    },
  });

  // Pie Chart
  new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
      labels: Object.keys(byCategory).map(
        (cat) => categoryIcon(cat) + " " + cat
      ),
      datasets: [
        {
          data: Object.values(byCategory),
          backgroundColor: [
            "#f87171",
            "#60a5fa",
            "#facc15",
            "#34d399",
            "#c084fc",
          ],
        },
      ],
    },
    options: {
      onClick: (e, elements) => {
        if (elements.length > 0) {
          const i = elements[0].index;
          alert(`You clicked on ${Object.keys(byCategory)[i]}`);
        }
      },
    },
  });

  // Bar Chart
  new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
      labels: Object.keys(bySubCategory),
      datasets: [
        {
          label: `Expenses (${currentCurrency})`,
          data: Object.values(bySubCategory),
          backgroundColor: "#38bdf8",
        },
      ],
    },
  });

  // Top 5
  const list = document.getElementById("topExpenses");
  list.innerHTML = "";
  sortedExpenses.slice(0, 5).forEach((exp) => {
    const amt = convert(exp.amount, exp.currency).toFixed(2);
    const li = document.createElement("li");
    li.textContent = `${categoryIcon(exp.category)} ${exp.category} > ${
      exp.subCategory
    }: ${currentCurrency} ${amt}`;
    list.appendChild(li);
  });
}

function destroyChart(id) {
  const chart = Chart.getChart(id);
  if (chart) chart.destroy();
}

function predictNextPeriods(last, count) {
  let [y, m] = last.split("-").map(Number);
  const result = [];
  for (let i = 0; i < count; i++) {
    m += 1;
    if (m > 12) {
      m = 1;
      y += 1;
    }
    result.push(`${y}-${m.toString().padStart(2, "0")}`);
  }
  return result;
}

function categoryIcon(cat) {
  const icons = {
    Housing: "🏠",
    Food: "🍔",
    Shopping: "🛒",
    Education: "🎓",
    Others: "📦",
  };
  return icons[cat] || "💰";
}

// Export

function exportCharts(format) {
  const charts = ["lineChart", "pieChart", "barChart"].map((id) =>
    document.getElementById(id)
  );
  if (format === "png") {
    charts.forEach((canvas, i) => {
      const link = document.createElement("a");
      link.download = `chart${i + 1}.png`;
      link.href = canvas.toDataURL();
      link.click();
    });
  } else if (format === "pdf") {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();
    charts.forEach((canvas, i) => {
      const imgData = canvas.toDataURL("image/png");
      if (i > 0) pdf.addPage();
      pdf.addImage(imgData, "PNG", 15, 40, 180, 100);
    });
    pdf.save("dashboard.pdf");
  }
}

// Add this function to handle shared data
function loadSharedData() {
  fetch("/api/shared-expenses")
    .then((response) => response.json())
    .then((data) => {
      const sharedDataList = document.getElementById("sharedDataList");
      sharedDataList.innerHTML = "";

      if (data.length === 0) {
        sharedDataList.innerHTML =
          '<p class="text-gray-500">No shared data available.</p>';
        return;
      }

      data.forEach((sharedData) => {
        const card = document.createElement("div");
        card.className = "card p-4 bg-white rounded-lg shadow";
        card.innerHTML = `
          <h3 class="font-semibold mb-2">Shared by ${sharedData.shared_by}</h3>
          <p class="text-sm text-gray-600 mb-2">Shared on ${
            sharedData.shared_at
          }</p>
          <button class="view-shared-data-btn bg-blue-500 text-white px-3 py-1 rounded"
                  data-expenses='${JSON.stringify(sharedData.expenses)}'>
              View Data
          </button>
        `;
        sharedDataList.appendChild(card);
      });

      // Add event listeners to view buttons
      document.querySelectorAll(".view-shared-data-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
          const expenses = JSON.parse(this.dataset.expenses);
          currentView = "shared";
          currentSharedData = expenses;
          drawCharts(expenses);

          // Show the switch button container
          const switchContainer = document.getElementById(
            "viewSwitchContainer"
          );
          switchContainer.style.display = "block";

          // Hide elements that should not be visible in shared view
          document.getElementById("dailySpendContainer").style.display = "none";
          document.getElementById("controlsContainer").style.display = "none";
        });
      });
    })
    .catch((error) => {
      console.error("Error loading shared data:", error);
    });
}

// Add this function to check for shared data on page load
function checkForSharedData() {
  const urlParams = new URLSearchParams(window.location.search);

  if (urlParams.get("view") === "shared") {
    const sharedExpenses = localStorage.getItem("sharedExpenses");

    if (sharedExpenses) {
      const expenses = JSON.parse(sharedExpenses);
      currentView = "shared";
      currentSharedData = expenses;
      drawCharts(expenses);

      // Show the switch button container
      const switchContainer = document.getElementById("viewSwitchContainer");
      if (switchContainer) {
        switchContainer.style.display = "block";
      }

      // Hide all elements that should not be visible in shared view
      document.getElementById("dailySpendContainer").style.display = "none";
      document.getElementById("controlsContainer").style.display = "none";
      document.getElementById("exportPNG").style.display = "none";
      document.getElementById("exportPDF").style.display = "none";
      document.getElementById("currencySelector").style.display = "none";

      // Hide all filter buttons
      document.querySelectorAll(".filter-btn").forEach((btn) => {
        btn.style.display = "none";
      });

      // Clear the localStorage after using it
      localStorage.removeItem("sharedExpenses");
    }
  }
}

// Add this near the beginning of the file, after variable declarations
document.addEventListener("DOMContentLoaded", function () {
  // Load personal data
  fetch("/api/expenses")
    .then((response) => response.json())
    .then((data) => {
      originalData = data;
      drawCharts(data);
    });

  // Check for shared data
  checkForSharedData();

  // Add event listener for back to personal button
  document
    .getElementById("backToPersonalBtn")
    .addEventListener("click", function () {
      currentView = "personal";
      drawCharts(originalData);
      document.getElementById("viewSwitchContainer").style.display = "none";
      document.getElementById("dailySpendContainer").style.display = "block";
      document.getElementById("controlsContainer").style.display = "flex";

      // Show all elements again
      document.getElementById("exportPNG").style.display = "inline-block";
      document.getElementById("exportPDF").style.display = "inline-block";
      document.getElementById("currencySelector").style.display = "block";

      // Show all filter buttons
      document.querySelectorAll(".filter-btn").forEach((btn) => {
        btn.style.display = "inline-block";
      });
    });
});
// Load shared data for the sidebar
loadSharedData();
