const expenseCtx = document.getElementById("expenseChart").getContext("2d");
const expenseChart = new Chart(expenseCtx, {
  type: "pie",
  data: {
    labels: [
      "Housing",
      "Food",
      "Transportation",
      "Entertainment",
      "Healthcare",
      "Others",
    ],
    datasets: [
      {
        data: [35, 20, 15, 10, 12, 8],
        backgroundColor: [
          "#3498db",
          "#2ecc71",
          "#f1c40f",
          "#e74c3c",
          "#9b59b6",
          "#1abc9c",
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "right",
      },
    },
  },
});

const incomeExpenseCtx = document
  .getElementById("incomeExpenseChart")
  .getContext("2d");
const incomeExpenseChart = new Chart(incomeExpenseCtx, {
  type: "bar",
  data: {
    labels: ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    datasets: [
      {
        label: "Income",
        data: [4200, 4500, 4300, 4800, 4600, 5000],
        backgroundColor: "#2ecc71",
      },
      {
        label: "Expenses",
        data: [3800, 4100, 3700, 4000, 4200, 3900],
        backgroundColor: "#e74c3c",
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

const trendCtx = document.getElementById("trendChart").getContext("2d");
const trendChart = new Chart(trendCtx, {
  type: "line",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Monthly Expenses",
        data: [
          3500, 3700, 3600, 3800, 3900, 3700, 3800, 4100, 3700, 4000, 4200,
          3900,
        ],
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.1)",
        fill: true,
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  },
});

const forecastCtx = document.getElementById("forecastChart").getContext("2d");
const forecastChart = new Chart(forecastCtx, {
  type: "line",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
      "Jan (Pred)",
      "Feb (Pred)",
      "Mar (Pred)",
    ],
    datasets: [
      {
        label: "Actual Expenses",
        data: [
          3500,
          3700,
          3600,
          3800,
          3900,
          3700,
          3800,
          4100,
          3700,
          4000,
          4200,
          3900,
          null,
          null,
          null,
        ],
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.1)",
        fill: true,
        tension: 0.3,
      },
      {
        label: "Predicted Expenses",
        data: [
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          3900,
          4100,
          4250,
          4400,
        ],
        borderColor: "#9b59b6",
        backgroundColor: "rgba(155, 89, 182, 0.1)",
        borderDash: [5, 5],
        fill: true,
        tension: 0.3,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  },
});
