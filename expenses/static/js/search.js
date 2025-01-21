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
      searchResults.innerHTML = ""; // Clear previous results

      // Perform AJAX POST request
      fetch("search-expenses", {
        method: "POST",
        body: JSON.stringify({ searchtext: searchValue }),
        // headers: {
        //   "Content-Type": "application/json",
        //   "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        // },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.length === 0)
          {

            console.log(data[0],'aaaa');
            searchResults.innerHTML = `
              <tr>
                <td colspan="6" class="text-center">No matching expenses found.</td>
              </tr>`;
          } else {
            data.forEach((expense) => {
                console.log(expense, ':expenses');
              searchResults.innerHTML += `
                <tr>
                
                  <td>${expense.amount}</td>
                  <td>${expense.category}</td>
                  <td>${expense.date}</td>
                  <td>${expense.description}</td>
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
