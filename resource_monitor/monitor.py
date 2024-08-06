from flask import Flask
import flask
import psutil
import humanize

disk_quota_cmd = ["quota", "-vs", "-p", "-w"]

app = Flask(
    'app', 
    template_folder="resource_monitor/template/",
    static_folder='resource_monitor/static'
)


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


print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(rule)

app.run(host='0.0.0.0', port=8080, debug=True)
