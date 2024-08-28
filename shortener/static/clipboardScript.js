document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");
    const clipboardShortenedBtn = document.getElementById("btn-shortened");
    const clipboardAnalyticsBtn = document.getElementById("btn-analytics");

    clipboardShortenedBtn.addEventListener("click", (event) => {
        let copyText = document.getElementById("clipboard-shortened").textContent;

        navigator.clipboard.writeText(copyText)
            .then(r => alert("Copied the text: " + copyText));
    });

    clipboardAnalyticsBtn.addEventListener("click", (event) => {
        let copyText = document.getElementById("clipboard-analytics").textContent;

        navigator.clipboard.writeText(copyText)
            .then(r => alert("Copied the text: " + copyText));
    });
});