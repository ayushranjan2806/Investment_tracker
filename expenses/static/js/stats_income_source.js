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

// Function to fetch chart data from the backend
const fetchChartData = async () => {
  try {
    const response = await fetch("income_source_summary"); // Update with the correct URL for income summary
    const results = await response.json();

    // Log the data to the console for debugging
    console.log("Data fetched from backend:", results);

    // Get chart data and labels from the fetched results
    chartData = Object.values(results.source_category_datasets); // Data values
    chartLabels = Object.keys(results.source_category_datasets); // Source labels

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
  currentChart = renderChart(ctx, "doughnut", chartData, chartLabels, "Income by Source (Donut)");
};

// Function to toggle charts based on button clicks
const toggleChart = (chartType, title) => {
  const ctx = document.getElementById("chartCanvas").getContext("2d");
  if (currentChart) currentChart.destroy(); // Destroy the current chart before rendering a new one
  currentChart = renderChart(ctx, chartType, chartData, chartLabels, title); // Render the new chart
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
  fetchChartData(); // Fetch the chart data when the page loads

  // Event listener for the Donut chart button
  document.getElementById("toggleDonut").addEventListener("click", () => {
    toggleChart("doughnut", "Income by Source (Donut)");
    setActiveButton("toggleDonut");
  });

  // Event listener for the Line chart button
  document.getElementById("toggleLine").addEventListener("click", () => {
    toggleChart("line", "Income Trend (Line)");
    setActiveButton("toggleLine");
  });

  // Event listener for the Bar chart button
  document.getElementById("toggleBar").addEventListener("click", () => {
    toggleChart("bar", "Income by Source (Bar)");
    setActiveButton("toggleBar");
  });
});
