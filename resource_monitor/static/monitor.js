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
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';

                        if (context.parsed !== null) {
                            label += `: ${context.parsed} ${unit}`;
                        }

                        return label;
                    }
                }
            }
        },
        animation: false,
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
        const table = document.getElementById("pid-chart");
        
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

            CpuData.datasets[0].data.push(roundDecimal(myCpuUsage, 2));
            CpuData.datasets[0].data.shift();
            CpuData.datasets[1].data.push(data.total.cpu.usage);
            CpuData.datasets[1].data.shift();

            updateCpuTxt(data)

            MemoryData.datasets[0].data.push(roundDecimal(myMemUsage / 10**9, 2));
            MemoryData.datasets[0].data.shift();
            MemoryData.datasets[1].data.push(roundDecimal(data.total.memory.used / 10**9, 2));
            MemoryData.datasets[1].data.shift();

            updateMemoryTxt(data);
        }
        
        // Display data in chart
        
        // CREDIT: Thanks stackoverflow
        // https://stackoverflow.com/questions/16270087/delete-all-rows-on-a-table-except-first-with-javascript
        var rows = table.rows;
        var i = rows.length;
        while (--i) {
            table.deleteRow(i);
        }

        data.by_pid.forEach((process) => {
            let newRow = table.insertRow(table.rows.length);
            newRow.insertCell(0).textContent = process.pid;
            newRow.insertCell(1).textContent = process.name;
            newRow.insertCell(2).textContent = process.cpu;
            newRow.insertCell(3).textContent = roundDecimal(process.memory / 10**9, 2);
            newRow.insertCell(4).textContent = process.status;
        });
        let totalRow = table.insertRow(table.rows.length);
        totalRow.insertCell(0).textContent = 'TOTAL:';
        totalRow.insertCell(1).textContent = '';
        totalRow.insertCell(2).textContent = myCpuUsage;
        totalRow.insertCell(3).textContent = roundDecimal(myMemUsage / 10**9, 2);
        totalRow.insertCell(4).textContent = '';
        
        console.log("updated graphs");
        chartCpu.update();
        chartMemory.update();
    });
}

function roundDecimal(number, roundTo) {
    return parseFloat((number).toFixed(roundTo))
}

function updateMemoryTxt(data) {
    const memoryStats = document.getElementById("memory-usage");
    
    if (memoryStats.matches(':hover')) {
        memoryStats.textContent = `${roundDecimal(data.total.memory.used / 10**9, 2)} GB / ${roundDecimal(data.total.memory.total / 10**9, 2)} GB`
    } else {
        memoryStats.textContent = data.total.memory.percent + "%";
    }
}

function updateCpuTxt(data) {
    const cpuStats = document.getElementById("cpu-usage");
    let myCpuUsage = 0;

    console.log(data)
    data.by_pid.forEach((process) => {
        myCpuUsage += process.cpu;
    });

    if (cpuStats.matches(':hover')) {
        cpuStats.textContent = `Global Usage: ${data.total.cpu.usage}%`
    } else {
        cpuStats.textContent = roundDecimal(myCpuUsage, 2) + "%";
    }
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
    labels: [],
    datasets: [{
        label: "Storage",
        data: [],
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

    const table = document.getElementById("pid-chart");

    const cpuStats = document.getElementById("cpu-usage");
    const memoryStats = document.getElementById("memory-usage");
    const storageStats = document.getElementById("storage-usage");

    // Get data
    fetch("/data")
    .then((response) => response.json())
    .then((data) => {
        console.log("Loaded global data");

        updateCpuTxt(data);
        updateMemoryTxt(data);
        storageStats.textContent = data.total.storage.percent + "%";

        const cpuGraph = new Chart("cpu-graph", {
            type: 'line',
            data: cpuData,
            options: getOptionData(null, true)
        });

        cpuStats.addEventListener("mouseover", (event) => {
            cpuStats.textContent = `Global Usage: ${data.total.cpu.usage}%`
        });

        cpuStats.addEventListener("mouseout", (event) => {
            let myCpuUsage = 0;
            console.log(data)
            data.by_pid.forEach((process) => {
                myCpuUsage += process.cpu;
            });
            cpuStats.textContent = roundDecimal(myCpuUsage, 2) + "%";
        });

        // We need global data to set this graph
        const memoryGraph = new Chart("memory-graph", {
            type: 'line',
            data: memoryData,
            options: getOptionData(2, true, roundDecimal(data.total.memory.total / 10**9, 2), " GB") // Round and convert to gb
        });

        memoryStats.addEventListener("mouseover", (event) => {
            memoryStats.textContent = `${roundDecimal(data.total.memory.used / 10**9, 2)} GB / ${roundDecimal(data.total.memory.total / 10**9, 2)} GB`;
        });

        memoryStats.addEventListener("mouseout", (event) => {
            memoryStats.textContent = data.total.memory.percent + "%";
        });

        let storageOptions = getOptionData(null, false, null, " GB")
        storageOptions.animation = true;
        storageOptions.plugins.tooltip.enabled = true;
        console.log(storageOptions)
        const storageGraph = new Chart("storage-graph", {
            type: 'doughnut',
            data: storageData,
            options: storageOptions
        });

        data.by_dir.forEach((directory) => {
            // Add storage data :D
            if (directory[1] == ".") { // Ignore the root filepath
                return
            }
            storageGraph.data.labels.push(directory[1]);
            storageGraph.data.datasets[0].data.push(directory[0] / 10**6);
        });
        storageGraph.update();

        setInterval(updateGraphs, 1000, cpuGraph, memoryGraph);
    });
});