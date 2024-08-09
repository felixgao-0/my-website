function getOptionData(limit, addScale) {
    let options = {
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxHeight: 8
                }
            }
        },
        spanGaps: true,
        animation: false
    }
    if (addScale) {
        options.scales = {
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
    if (limit !== null) {
        options.plugins.annotation = {
            annotations: [{
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                yMin: limit,
                yMax: limit,
                borderColor: 'red',
                borderWidth: 2,
                label: {
                    content: 'Threshold'
                }
            }]
        }
    }
    return options
}

function updateGraphs(chartCpu, chartMemory) {
    fetch("/data/global")
    .then((response) => response.json())
    .then((globalData) => {
        CpuData = chartCpu.data;
        CpuData.labels.push("");
        CpuData.datasets[1].data.push(globalData.cpu.usage);
        CpuData.datasets[1].data.shift();
        CpuData.labels.shift();

        chartCpu.update();
        
        cpuStats = document.getElementById("cpu-usage");
        cpuStats.textContent = globalData.cpu.usage + "%";


        MemoryData = chartMemory.data;
        MemoryData.labels.push("");
        MemoryData.datasets[1].data.push(globalData.memory.percent);
        MemoryData.datasets[1].data.shift();
        MemoryData.labels.shift();

        chartMemory.update();

        memStats = document.getElementById("memory-usage");
        memStats.textContent = globalData.memory.percent + "%";
    });
}

const cpuData = {
    labels: Array(30).fill(null),
    datasets: [{
        label: 'My Usage',
        data: Array(30).fill(null),
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)'
    }, {
        label: 'Global Usage',
        data: Array(30).fill(null),
        fill: true,
        backgroundColor: 'rgba(201, 203, 207, 0.2)',
        borderColor: 'rgba(201, 203, 207, 1)'
    }]
}

const memoryData = {
    labels: Array(30).fill(null),
    datasets: [{
        label: 'My Usage',
        data: Array(30).fill(null),
        fill: true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)'
    }, {
        label: 'Global Usage',
        data: Array(30).fill(null),
        fill: true,
        backgroundColor: 'rgba(201, 203, 207, 0.2)',
        borderColor: 'rgba(201, 203, 207, 1)'
    }]
}

const storageData = {
    labels: Array(30).fill(null),
    datasets: [{
        label: "Storage",
        data: Array(30).fill(null),
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

    const cpuStats = document.getElementById("cpu-usage");
    const memoryStats = document.getElementById("memory-usage");
    const storageStats = document.getElementById("storage-usage");

    // Global data
    fetch("/data/global")
    .then((response) => response.json())
    .then((globalData) => {
        console.log("Loaded global data");

        cpuStats.textContent = globalData.cpu.usage + "%";
        memoryStats.textContent = globalData.memory.percent + "%";
        storageStats.textContent = globalData.storage.percent + "%";
    });

    const cpuGraph = new Chart("cpu-graph", {
        type: 'line',
        data: cpuData,
        options: getOptionData(null, true)
    });

    const memoryGraph = new Chart("memory-graph", {
        type: 'line',
        data: memoryData,
        options: getOptionData(2, true)
    });

    const storageGraph = new Chart("storage-graph", {
        type: 'doughnut',
        data: storageData,
        options: getOptionData(null, false)
    });

    setInterval(updateGraphs, 1000, cpuGraph, memoryGraph);
});