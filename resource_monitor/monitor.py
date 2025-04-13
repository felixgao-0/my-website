"""
Nest Resouce Monitor - Backend: This runs a flask server to run the site's backend with psutil
"""

import os
import subprocess

import flask
import psutil
import redis
from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# import global_utils

# from flask_socketio import SocketIO

# Load my .env file :)
load_dotenv()

app = Flask(
    "app",
    template_folder="resource_monitor/template/",
    static_folder="resource_monitor/static",
)
# app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
# socketio = SocketIO(app)

# Limit the requests to prevent DDoS from the inside
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",
)

# Add emojis cause they look nice
status_emojis = {
    "running": "🏃",
    "sleeping": "😴",
    "zombie": "🧟",
    "stopped": "⏹️",
    "disk-sleep": "💽",
}


def get_storage():
    result = subprocess.run(
        ["du", "--max-depth=1", "-c", "-b", os.getcwd()],
        capture_output=True,
        text=True,
        check=True,
    )
    new_result = []
    for file_path in result.stdout.splitlines():
        split = file_path.split("\t")
        new_result.append(split)  # Add item to dict

    return new_result


def check_redis_connection() -> bool:
    """
    This function checks if redis is connected, using the redis module.

    Returns:
        `bool` - if redis server is running on port 6379 or not.
    """
    try:
        r = redis.Redis(host="localhost", port=6379)
        r.ping()
        return True
    except redis.ConnectionError as e:
        print(f"Redis connection error: {e}")
        print("Please start redis and try again.")
        return False
    except redis.TimeoutError as e:
        print(f"Redis timeout error: {e}")
        print("Connection to Redis timed out.")
        return False
    except Exception as e:
        print(f"Unexpected error connecting to Redis: {e}")
        return False


@app.route("/")
def index():
    return flask.render_template("monitor.html")


"""
@app.route("/run_commands")
def get_cmd_data():
    # Nest cli not in replit so commented out ):
    #nest_cli = subprocess.run(
    #    ["nest", "resources"],
    #    capture_output=True, 
    #    text=True
    #)

    sys_vitals = subprocess.run(
        ["top" , "-n1" , "-b"],
        capture_output=True, 
        text=True
    )

    return {
        "top": sys_vitals.stdout,
        "nest": 'Disk usage: 0.0 GB used out of 15.0 GB limit\nMemory usage: 0.05 GB used out of 2.0 GB limit\n' # Sample response from the nest cli cause this is replit
    }
"""


@app.route("/data")
@limiter.limit("3 per second")
def data_pid():
    memory = psutil.virtual_memory()
    storage = psutil.disk_usage("/")
    total_mem = 0
    total_cpu = 0

    try:
        stats: dict = {
            "by_pid": [],
            "total": {
                "cpu": {
                    "usage": psutil.cpu_percent(interval=0.1),
                    "frequency": psutil.cpu_freq().current,
                    "per-core": psutil.cpu_percent(interval=0.1, percpu=True),
                },
                "memory": {
                    "total": memory.total,
                    "used": memory.used,
                    # "free": memory.available,
                    "percent": memory.percent,
                },
                "storage": {
                    "total": storage.total,
                    "used": storage.used,
                    "free": storage.free,
                    "percent": storage.percent,
                },
            },
            "by_dir": get_storage(),
            "total_cpu": total_cpu,
            "total_mem": total_mem,
        }

        for process in psutil.process_iter():
            stats["by_pid"].append(
                {
                    "pid": process.pid,
                    "name": process.name(),
                    "cpu": process.cpu_percent(interval=0.1),
                    "memory": process.memory_full_info().uss,
                    "shared": process.memory_full_info().shared,
                    "status": f"{process.status()} ({status_emojis.get(process.status())})",
                }
            )
            total_cpu += process.cpu_percent()
            total_mem += process.memory_info().rss
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        # Skip processes that are gone/no access
        pass

    return stats


def main():
    if check_redis_connection():
        app.run(
            host="localhost", port=int(os.environ["PORT_RESOURCE_MONITOR"]), debug=False
        )


if __name__ == "__main__":
    main()
