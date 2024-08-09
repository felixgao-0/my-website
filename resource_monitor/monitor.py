from flask import Flask
import flask
import psutil

disk_quota_cmd = ["quota", "-vs", "-p", "-w"]

app = Flask(
    'app', 
    template_folder="resource_monitor/template/",
    static_folder='resource_monitor/static'
)


@app.route('/')
def index():
    return flask.render_template("monitor.html")


@app.route('/data')
def data_pid():
    stats: dict = {"by_pid": {}, "total": {}}
    memory = psutil.virtual_memory()
    storage = psutil.disk_usage('/')

    total_cpu: int = 0
    total_mem: int = 0

    for pid in psutil.pids():
        process = psutil.Process(pid)
        stats["by_pid"][f"{pid}"] = {
            "name": process.name(),
            "cpu": process.cpu_percent(),
            "memory": process.memory_info().rss,
            "status": process.status()
        }
        total_cpu += process.cpu_percent()
        total_mem += process.memory_info().rss

    stats["total"]["cpu"] = {
        "usage": psutil.cpu_percent(),
        "frequency": psutil.cpu_freq().current,
        "per-core": psutil.cpu_percent(percpu=True)
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
