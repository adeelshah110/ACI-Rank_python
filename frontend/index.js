let filesRead = 0;
let results = {};

function onStart() {
    toggleVisibility(false);
    document.getElementById("msg").innerText = "Loading...";
    fetchResults();
}

function toggleVisibility(show) {
    const sections = ["buttons_section", "output_section"];
    sections.forEach(id => {
        document.getElementById(id).style.display = show ? "block" : "none";
    });
}

function fetchResults() {
    const url = document.getElementById("input_url").value;
    if (!url) return alert("Please enter a valid URL.");

    fetch(`get_dom.php?url=${encodeURIComponent(url)}`)
        .then(response => response.text())
        .then(data => {
            results = JSON.parse(data);
            toggleVisibility(true);
            displayOutput("keywords");
        })
        .catch(error => console.error("Error fetching results:", error));
}

function displayOutput(type) {
    const content = results[type] || "No data available.";
    document.getElementById("output_content").innerText = content;
}
