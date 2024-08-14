import subprocess
import threading
import os
import time

from flask import Flask
import flask

import psutil

app = Flask(
    'app', 
    template_folder="resource_monitor/template/",
    static_folder='resource_monitor/static'
)

print(f"Current directory: {os.getcwd()}")

# Add emojis cause they look nice
status_emojis = {
    "running": "🏃",
    "sleeping": "😴",
    "zombie": "🧟",
    "stopped": "⏹️",
    "disk-sleep": "💽"
}

def get_storage():
    result = subprocess.run(
        ["du", "--max-depth=1", "-c", os.getcwd()],
        capture_output=True, 
        text=True
    )
    new_result = []
    for file_path in result.stdout.splitlines():
        split = file_path.split("\t")
        new_result.append(split) # Add item to dict

    return new_result


@app.route('/')
def index():
    return flask.render_template("monitor.html")


@app.route("/run_commands")
def get_cmd_data():
    """ Nest cli not in replit so commented out ):
    nest_cli = subprocess.run(
        ["nest", "resources"],
        capture_output=True, 
        text=True
    )"""

    sys_vitals = subprocess.run(
        ["top" , "-n1" , "-b"],
        capture_output=True, 
        text=True
    )

    return {
        "top": sys_vitals.stdout,
        "nest": 'Disk usage: 0.0 GB used out of 15.0 GB limit\nMemory usage: 0.05 GB used out of 2.0 GB limit\n' # Sample response from the nest cli cause this is replit
    }
    

@app.route('/data')
def data_pid():
    stats: dict = {"by_pid": [], "total": {}, "by_dir": []}
    memory = psutil.virtual_memory()
    storage = psutil.disk_usage('/')

    total_cpu: float = 0
    total_mem: float = 0

    for process in psutil.process_iter():
        stats["by_pid"].append({
            "pid": process.pid,
            "name": process.name(),
            "cpu": process.cpu_percent(),
            "memory": process.memory_info().rss,
            "status": f"{process.status()} ({status_emojis.get(process.status())})"
        })
        total_cpu += process.cpu_percent()
        total_mem += process.memory_info().rss

    stats["by_dir"] = get_storage()

    stats["total"]["cpu"] = {
        "usage": psutil.cpu_percent(interval=0.1),
        "frequency": psutil.cpu_freq().current,
        "per-core": psutil.cpu_percent(interval=0.1, percpu=True)
    }
    stats["total"]["memory"] = {
        "free": memory.available,
        "used": memory.used,
        "total": memory.total,
        "percent": memory.percent
    }
    stats["total"]["storage"] = {
        "total": storage.total,
        "used": storage.used,
        "free": storage.free,
        "percent": storage.percent
    }
    stats["total_cpu"] = total_cpu
    stats["total_mem"] = total_mem

    #data = stats

    return stats

    # Make data update every second, on the second
    # CREDIT: thx chatgpt for the help
    """
    now = time.time()
    next_second = (now // 1 + 1)
    wait_time = next_second - now
    time.sleep(wait_time)
    """

app.run(host='0.0.0.0', port=8080, debug=True)
