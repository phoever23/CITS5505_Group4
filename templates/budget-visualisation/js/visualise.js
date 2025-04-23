
document.getElementById('csvFile').addEventListener('change', function (e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (event) {
    const text = event.target.result;
    const data = parseCSV(text);
    drawCharts(data);
  };
  reader.readAsText(file);
});

function parseCSV(csvText) {
  const lines = csvText.trim().split('\n');
  const headers = lines[0].split(',');
  return lines.slice(1).map(line => {
    const values = line.split(',');
    return {
      date: values[0],
      category: values[1],
      subCategory: values[2],
      amount: parseFloat(values[3]),
      currency: values[4]
    };
  });
}

function drawCharts(data) {
  const byMonth = {};
  const byCategory = {};
  const bySubCategory = {};
  const sortedExpenses = [...data].sort((a, b) => b.amount - a.amount);

  data.forEach(entry => {
    const month = entry.date.slice(0, 7);
    byMonth[month] = (byMonth[month] || 0) + entry.amount;
    byCategory[entry.category] = (byCategory[entry.category] || 0) + entry.amount;
    bySubCategory[entry.subCategory] = (bySubCategory[entry.subCategory] || 0) + entry.amount;
  });

  new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
      labels: Object.keys(byMonth),
      datasets: [{
        label: 'Monthly Expenses',
        data: Object.values(byMonth),
        borderColor: 'orange',
        backgroundColor: 'rgba(255,165,0,0.2)',
        tension: 0.3,
        fill: true
      }]
    }
  });

  new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
      labels: Object.keys(byCategory),
      datasets: [{
        data: Object.values(byCategory),
        backgroundColor: ['#f87171', '#60a5fa', '#facc15', '#34d399', '#c084fc']
      }]
    }
  });

  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(bySubCategory),
      datasets: [{
        label: 'Expenses by Sub-Category',
        data: Object.values(bySubCategory),
        backgroundColor: '#38bdf8'
      }]
    }
  });

  const list = document.getElementById('topExpenses');
  list.innerHTML = '';
  sortedExpenses.slice(0, 5).forEach(exp => {
    const li = document.createElement('li');
    li.textContent = `${exp.category} > ${exp.subCategory}: $${exp.amount}`;
    list.appendChild(li);
  });
}
