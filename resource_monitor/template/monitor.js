globalGraphData = {
    "x": [],
    "y": []
}

/*
const myGraph = new Chart("my-graph", {
    type: "line",
    data: {},
    options: {}
}); */

const globalGraph = new Chart("global-graph", {
    type: "line",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor:"rgba(0,0,255,1.0)",
            borderColor: "rgba(0,0,255,0.1)",
            data: yValues
        }],
    options: {}
});