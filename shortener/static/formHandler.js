document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded, yay");
    // Hi Arcade reviewers! I hope you have a good end of Arcade day! More tickets pls? /s

    const form = document.getElementById("create-url-form");

    // Enable submission upon agreement to my tos hehe
    form.addEventListener("click", (event) => {
        document.getElementById("submit-btn").disabled = !document.getElementById("confirm-checkbox").checked;
    });
});