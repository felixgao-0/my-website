const globalGraph = new Chart("cpu-graph", {
    type: 'line',
    data: {
        labels: ['12:45:40', '12:45:41', '12:45:42', '12:45:43'],
        datasets: [{
            label: 'My Usage',
            data: [10, 11.5, 14, 13.87],
            hoverBorderWidth: 1,
            hoverBorderColor: 'rgba(0, 0, 0, 0.1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)'
        }, {
            label: 'Global Usage',
            data: [50.67, 53.89, 53.63, 48.79],
            hoverBorderWidth: 1,
            hoverBorderColor: 'rgba(0, 0, 0, 0.1)',
            backgroundColor: 'rgba(201, 203, 207, 0.2)',
            borderColor: 'rgba(201, 203, 207, 1)'
        }]
    },
    options: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                usePointStyle: true,
                boxWidth: 6,
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                    max: 100,
                    callback: function(value) {
                        return value + '%';
                    }
                }
            }]
        }
    }
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