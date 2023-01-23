async function showAllProducts() {
    try {
      const response = await fetch('http://localhost:5000/all');
      const data = await response.json();
      let results = "";
      for (let i = 0; i < data.length; i++) {
        results += `<div class="result" onclick="window.location.href='${data[i].link}';">
          <img src="${data[i].image}" width="100" height="100">
        </div>`;
      }
      document.getElementById("results-container").innerHTML = results;
    } catch (err) {
      console.error(err);
    }
  }
  async function search() {
    try {
      const keyword = document.getElementById("search-input").value;
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
                      'Content-Type': 'application/json'
        },
        body: JSON.stringify({keyword})
      });
      const data = await response.json();
      let results = "";
      if (data.length > 0) {
        for (let i = 0; i < data.length; i++) {
          results += `<div class="result" onclick="window.location.href='${data[i].link}';">
            <img src="${data[i].image}" width="100" height="100">
          </div>`;
        }
      } else {
        results = "No results found.";
      }
      document.getElementById("results-container").innerHTML = results;
    } catch (err) {
      console.error(err);
    }
  }