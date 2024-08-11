function getOptionData(limit, addScale, scaleMax = 100, unit = "%") {
    let options = {
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxHeight: 8
                }
            },
            tooltip: {
                enabled: false, // Disable tooltips
            }
        },
        animation: false,
        tension: 0.1,
        elements: {
            point: {
                radius: 0 // default to disabled in all datasets
            }
        }
    }
    if (addScale) {
        options.scales = {
            y: {
                min: 0,
                max: scaleMax,
                ticks: {
                    callback: function(value) {
                        return value + unit;
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
    fetch("/data")
    .then((response) => {
        if (response.status === 200) {
            return response.json()
        } else {
            console.warn(`Couldn't fetch global data - HTTP ${response.status}`)
            return null
        }
    })
    .then((data) => {
        let CpuData = chartCpu.data;
        let MemoryData = chartMemory.data;

        let myCpuUsage = 0;
        let myMemUsage = 0;

        CpuData.labels.push("");
        CpuData.labels.shift();

        MemoryData.labels.push("");
        MemoryData.labels.shift();

        if (data === null) {
            CpuData.datasets[0].data.push(null);
            CpuData.datasets[0].data.shift();
            CpuData.datasets[1].data.push(null);
            CpuData.datasets[1].data.shift();

            MemoryData.datasets[0].data.push(null);
            MemoryData.datasets[0].data.shift();
            MemoryData.datasets[1].data.push(null);
            MemoryData.datasets[1].data.shift();
        } else {
            data.by_pid.forEach((process) => {
                myCpuUsage += process.cpu;
                myMemUsage += process.memory;
            });

            CpuData.datasets[0].data.push(myCpuUsage);
            CpuData.datasets[0].data.shift();
            CpuData.datasets[1].data.push(data.total.cpu.usage);
            CpuData.datasets[1].data.shift();

            cpuStats = document.getElementById("cpu-usage");
            cpuStats.textContent = data.total.cpu.usage + "%";

            MemoryData.datasets[0].data.push(roundDecimal(myMemUsage / 10**9, 2));
            MemoryData.datasets[0].data.shift();
            MemoryData.datasets[1].data.push(roundDecimal(data.total.memory.used / 10**9, 2));
            MemoryData.datasets[1].data.shift();

            memStats = document.getElementById("memory-usage");
            memStats.textContent = data.total.memory.percent + "%";
        }
        console.log("updated graphs");
        chartCpu.update();
        chartMemory.update();
    });
}

function roundDecimal(number, roundTo) {
    return parseFloat((number).toFixed(roundTo))
}

const cpuData = {
    labels: Array(30).fill(""),
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
    labels: Array(30).fill(""),
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

    // Get data
    fetch("/data")
    .then((response) => response.json())
    .then((data) => {
        console.log("Loaded global data");

        cpuStats.textContent = data.total.cpu.usage + "%";
        memoryStats.textContent = data.total.memory.percent + "%";
        storageStats.textContent = data.total.storage.percent + "%";

        const cpuGraph = new Chart("cpu-graph", {
            type: 'line',
            data: cpuData,
            options: getOptionData(null, true)
        });

        // We need global data to set this graph
        const memoryGraph = new Chart("memory-graph", {
            type: 'line',
            data: memoryData,
            options: getOptionData(2, true, roundDecimal(data.total.memory.total / 10**9, 2), " GB") // Round and convert to gb
        });

        const storageGraph = new Chart("storage-graph", {
            type: 'doughnut',
            data: storageData,
            options: getOptionData(null, false)
        });

        memoryStats.addEventListener("mouseover", (event) => {
            memoryStats.textContent = `${roundDecimal(data.total.memory.used / 10**9, 2)} GB /${roundDecimal(data.total.memory.total / 10**9, 2)} GB`
        });

        memoryStats.addEventListener("onmouseout", (event) => {
            memoryStats.textContent = data.total.memory.percent + "%";
        });

        setInterval(updateGraphs, 1000, cpuGraph, memoryGraph);
    });
});