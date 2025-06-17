const API_URL = "http://localhost:5000/predict";

async function checkToxicity(text) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return await response.json();
}

// Scan comments every 2 seconds (YouTube loads dynamically)
setInterval(async () => {
  document.querySelectorAll("#content-text").forEach(async (comment) => {
    if (comment.dataset.checked) return; // Skip already processed

    const result = await checkToxicity(comment.textContent);
    if (result.is_toxic) {
      comment.style.backgroundColor = "#ffcccc";
      comment.insertAdjacentHTML("beforeend", " ⚠️ Toxic");
    }
    comment.dataset.checked = "true";
  });
}, 2000);
