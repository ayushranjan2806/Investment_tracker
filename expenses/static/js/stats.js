// Function to render a chart
const renderChart = (ctx, type, data, labels, title) => {
  return new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: [
        {
          label: title,
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: title,
        },
      },
    },
  });
};

// Variables to store chart data and the current chart instance
let chartData = null;
let chartLabels = null;
let currentChart = null;

// Function to fetch chart data
const fetchChartData = async () => {
  try {
    const response = await fetch("/expense_category_summary");
    const results = await response.json();
    console.log(results);
    chartData = Object.values(results.expense_category_datasets);
    console.log(chartData);
    chartLabels = Object.keys(results.expense_category_datasets);

    // Render the default chart (Donut)
    renderDefaultChart();
  } catch (error) {
    console.error("Error fetching chart data:", error);
  }
};

// Function to render the default Donut chart
const renderDefaultChart = () => {
  const ctx = document.getElementById("chartCanvas").getContext("2d");
  if (currentChart) currentChart.destroy();
  currentChart = renderChart(ctx, "doughnut", chartData, chartLabels, "Expenses by Category (Donut)");
};

// Function to toggle charts based on button clicks
const toggleChart = (chartType, title) => {
  const ctx = document.getElementById("chartCanvas").getContext("2d");
  if (currentChart) currentChart.destroy();
  currentChart = renderChart(ctx, chartType, chartData, chartLabels, title);
};

// Set active button and toggle chart
const setActiveButton = (activeButtonId) => {
  document.querySelectorAll(".btn-group button").forEach((button) => {
    button.classList.remove("active", "btn-primary");
    button.classList.add("btn-outline-primary");
  });
  const activeButton = document.getElementById(activeButtonId);
  activeButton.classList.remove("btn-outline-primary");
  activeButton.classList.add("active", "btn-primary");
};

// Add event listeners for the toggle buttons
document.addEventListener("DOMContentLoaded", () => {
  fetchChartData();

  document.getElementById("toggleDonut").addEventListener("click", () => {
    toggleChart("doughnut", "Expenses by Category (Donut)");
    setActiveButton("toggleDonut");
  });

  document.getElementById("toggleLine").addEventListener("click", () => {
    toggleChart("line", "Expenses Trend (Line)");
    setActiveButton("toggleLine");
  });

  document.getElementById("toggleBar").addEventListener("click", () => {
    toggleChart("bar", "Expenses by Category (Bar)");
    setActiveButton("toggleBar");
  });
});
