// CREDIT: tysm freeCodeCamp
// https://www.freecodecamp.org/news/how-to-validate-urls-in-javascript/
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (err) {
        return false;
    }
}

function createUrl(event) {
    event.preventDefault();
    const originalUrl = document.getElementById('original-link-field');
    const newUrl = document.getElementById('shortened-link-field');

    console.log("Validating data before submitting form :D")

    // This regex matches dashes, underscores, numbers and letters only
    let newUrlRegex = /^[a-zA-Z0-9_-]+$/;

    if  (!isValidUrl(originalUrl.value)) {
        // TODO: Present error to user :noo:
    }

    if  (!newUrlRegex.test(newUrl.value)) {
        // TODO: Present error to user :noo:
    }

    document.getElementById("create-url-form").submit();
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    const form = document.getElementById("create-url-form");

    //form.addEventListener("submit", (event) => {
    //    createUrl(event);
    //});

    // Enable submission upon agreement to my tos muahaha
    form.addEventListener("click", (event) => {
        document.getElementById("submit-btn").disabled = !document.getElementById("confirm-checkbox").checked;
    });
});