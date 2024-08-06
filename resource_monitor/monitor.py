from flask import Flask
import flask
import psutil
import humanize
import os

print(os.getcwd())

disk_quota_cmd = ["quota", "-vs", "-p", "-w"]


app = Flask('app', template_folder="resource_monitor/template/")

def get_cpu():
    stats: dict = {}
    for pid in psutil.pids():
        process = psutil.Process(pid)
        stats[pid] = {
            "name": p.name(),
            "cpu": process.cpu_percent(),
            "memory": process.memory_info().rss
        }
    return stats


@app.route('/')
def index():
    print(get_cpu())
    return flask.render_template("monitor.html")

@app.route('/cpu')
def cpu():
    return str(psutil.cpu_percent())

@app.route('/memory')
def memory():
    return str(psutil.virtual_memory())

app.run(host='0.0.0.0', port=8080)
