async function get_pid() {
    const response = await fetch("/data/pid");
    return await response.json();
}

async function get_global() {
    const response = await fetch("/data/global");
    return await response.json();
}

/*
const myGraph = new Chart("my-graph", {
    type: "line",
    data: {},
    options: {}
});*/

const globalGraph = new Chart("global-graph", {
    type: "line",
    data: {
        labels: ["1", "2", "3"],
        datasets: [{
            backgroundColor:"rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: ["60%", "75%", "90%"]
        }]
    },
    options: {}
});

function setGlobalStorageBar(amount) {
    var elem = document.getElementById("global-storage-bar");
    elem.style.width = amount + "%";
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    // Global data
    fetch("/data/global")
    .then((response) => response.json())
    .then((globalData) => {
        let amount = globalData.storage.percent
        const globalProgressBar = document.getElementById("global-storage-bar");
        globalProgressBar.textContent = amount + "%";
        globalProgressBar.style.width = amount + "%";
    });
});