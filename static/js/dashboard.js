// ✅ Final version of dashboard.js with locked categories, subcategories, and currencies

let originalData = [];
let currentFilter = "monthly";
let currentCurrency = "USD";
const budgetTarget = 2000;

const allowedCategories = {
  Housing: ["rent", "mortgage"],
  Food: ["grocery", "restaurants"],
  Shopping: ["clothes", "electronics"],
  Education: ["tuition", "printing"],
  Others: ["gifts", "transport", "maintenance"],
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
          data: Array(periods.length + 3).fill(budgetTarget),
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
