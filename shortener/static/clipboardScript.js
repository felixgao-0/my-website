document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");
    const clipboardShortenedBtn = document.getElementById("btn-shortened");
    const clipboardAnalyticsBtn = document.getElementById("btn-analytics");

    clipboardShortenedBtn.addEventListener("click", (event) => {
        let copyText = document.getElementById("clipboard-shortened").textContent;
        clipboardShortenedBtn.textContent = 'check';

        navigator.clipboard.writeText(copyText)
            .then(r => setTimeout(() => {
                clipboardShortenedBtn.textContent = 'content_paste';
            }, 800)); // Revert checkmark back to clipboard icon
    });

    clipboardAnalyticsBtn.addEventListener("click", (event) => {
        let copyText = document.getElementById("clipboard-analytics").textContent;
        clipboardAnalyticsBtn.textContent = 'check';

        navigator.clipboard.writeText(copyText)
            .then(r => setTimeout(() => {
                clipboardAnalyticsBtn.textContent = 'content_paste';
            }, 800)); // Revert checkmark back to clipboard icon
    });
});