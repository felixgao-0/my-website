const globalGraph = new Chart("cpu-graph", {
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

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    // Global data
    fetch("/data/global")
    .then((response) => response.json())
    .then((globalData) => {
        //Nothing for now
    });
});