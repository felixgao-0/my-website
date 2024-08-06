from flask import Flask
import flask
import psutil
import humanize
import os

print(os.getcwd())

disk_quota_cmd = ["quota", "-vs", "-p", "-w"]

app = Flask('app', template_folder="resource_monitor/template/")


def get_stats_by_pid():
    stats: dict = {}
    for pid in psutil.pids():
        process = psutil.Process(pid)
        stats[f"{pid}"] = {
            "name": process.name(),
            "cpu": process.cpu_percent(),
            "memory": process.memory_info().rss,
            "status": process.status()
        }
    return stats


@app.route('/')
def index():
    return flask.render_template("monitor.html")


@app.route('/static/<path:filepath>')
def get_js(filepath):
    return flask.send_from_directory('resource_monitor/site_files/', filepath)


@app.route('/data/pid')
def data_pid():
    return get_stats_by_pid()


@app.route('/data/global')
def data_global():
    memory = psutil.virtual_memory()
    storage = psutil.disk_usage('/')
    data = {
        "cpu": {
            "usage": psutil.cpu_percent(),
            "frequency": psutil.cpu_freq(),
            "per-core": psutil.cpu_percent(percpu=True)
        },
        "memory": {
            "free": memory.available,
            "used": memory.used,
            "total": memory.total,
            "percent": memory.percent
        },
        "storage": {
            "total": storage.total,
            "used": storage.used,
            "free": storage.free,
            "percent": storage.percent
        }
    }
    return data


"""
psutil.cpu_percent()
psutil.virtual_memory()
"""

app.run(host='0.0.0.0', port=8080)
