document.addEventListener("DOMContentLoaded", () => {
  const searchField = document.querySelector("#search-field");
  const tableOutput = document.querySelector("#search-table");
  tableOutput.style.display = "none";

  const defaultTable = document.querySelector("#default-table");
  const searchResults = document.querySelector("#search-results");

  // Initially hide the search results table
  tableOutput.style.display = "none";

  searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value.trim();

    if (searchValue.length > 0) {
      // Hide the default table
      defaultTable.style.display = "none";
      tableOutput.style.display = "block";
        searchResults.innerHTML = "";

      // Perform AJAX POST request
      fetch("search-income", {
        method: "POST",
        body: JSON.stringify({ searchtext: searchValue }),

      })
        .then((response) => response.json())
        .then((data) => {
          if (data.length === 0) {

            searchResults.innerHTML = `
              <tr>
                <td colspan="6" class="text-center">No matching income found.</td>
              </tr>`;
          } else {
            // console.log(data)
            data.forEach((income) => {
              searchResults.innerHTML += `
                <tr>
                  <td>${income.amount}</td>
                  <td>${income.source}</td>
                  <td>${income.date}</td>
                  <td>${income.description}</td>
                </tr>`;
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      // Show the default table when the search field is empty
      defaultTable.style.display = "block";
      tableOutput.style.display = "none";
    }
  });
});
