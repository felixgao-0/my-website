from flask import Flask
import psutil
import os

print(os.getcwd())

psutil.PROCFS_PATH = os.getcwd()

disk_quota_cmd = ["quota", "-vs", "-p", "-w"]


app = Flask('app')


@app.route('/cpu')
def cpu():
  return str(psutil.cpu_percent())

@app.route('/memory')
def memory():
  return str(psutil.virtual_memory())

app.run(host='0.0.0.0', port=8080)
