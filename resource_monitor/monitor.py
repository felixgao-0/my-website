from flask import Flask
import flask
import psutil
import subprocess

app = Flask(
    'app', 
    template_folder="resource_monitor/template/",
    static_folder='resource_monitor/static'
)


def get_storage():
    result = subprocess.run(["du", "-S"], shell=True, capture_output=True, text=True)
    result_dict = result.stdout.splitlines()
    for file_path in result_dict:
        print(file_path)
        
@app.route('/')
def index():
    get_storage()
    return flask.render_template("monitor.html")


@app.route('/data')
def data_pid():
    stats: dict = {"by_pid": [], "total": {}}
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
            "status": process.status()
        })
        total_cpu += process.cpu_percent()
        total_mem += process.memory_info().rss

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
    return stats


app.run(host='0.0.0.0', port=8080, debug=True)
