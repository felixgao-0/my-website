function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

const options = {
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                usePointStyle: true,
                pointStyle: 'circle',
                boxHeight: 8
            }
        },
        annotation: {
            annotations: [{
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                yMin: 50,
                yMax: 50,
                borderColor: 'red',
                borderWidth: 2,
                label: {
                    content: 'Threshold'
                }
            }]
        }
    },
    scales: {
        y: {
            min: 0,
            max: 100,
            ticks: {
                callback: function(value) {
                    return value + '%';
                }
            }
        }
    }
}

const cpuData = {
    labels: ['12:45:40', '12:45:41', '12:45:42', '12:45:43'],
    datasets: [{
        label: 'My Usage',
        data: [10, 11.5, 14, 13.87],
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)'
    }, {
        label: 'Global Usage',
        data: [50.67, 53.89, 53.63, 48.79],
        fill: true,
        backgroundColor: 'rgba(201, 203, 207, 0.2)',
        borderColor: 'rgba(201, 203, 207, 1)'
    }]
}

const memoryData = {
    labels: ['12:45:40', '12:45:41', '12:45:42', '12:45:43'],
    datasets: [{
        label: 'My Usage',
        data: [0.5, 0.67, 1, 1.43],
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)'
    }, {
        label: 'Global Usage',
        data: [50.67, 48.32, 49.65, 45.87],
        fill: true,
        backgroundColor: 'rgba(201, 203, 207, 0.2)',
        borderColor: 'rgba(201, 203, 207, 1)'
    }]
}

const storageData = {
    labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    datasets: [{
        label: "Storage",
        data: [12, 54, 32, 54, 34, 32, 57, 87, 32, 14, 23, 56],
        fill: true,
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 203, 92)',
            'rgb(255, 163, 26)',
            'rgb(92, 185, 94)',
            'rgb(165, 56, 182)'
            ],
        hoverOffset: 15,
        borderColor: 'rgba(54, 162, 235, 1)'
    }]
}


document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM has fully loaded");

    // Global data
    fetch("/data/global")
    .then((response) => response.json())
    .then((globalData) => {
        //Nothing for now
    });

    const cpuGraph = new Chart("cpu-graph", {
        type: 'line',
        data: cpuData,
        options: options
    });

    const memoryGraph = new Chart("memory-graph", {
        type: 'line',
        data: memoryData,
        options: options
    });

    const storageGraph = new Chart("storage-graph", {
        type: 'doughnut',
        data: storageData,
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxHeight: 8
                    }
                }
            }
        }
    });
});