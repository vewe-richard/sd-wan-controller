from controllerv2.core import Singleton

from flask import render_template
from flask import Flask, request
import sys

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
@app.route("/index.htm")
def index():
    region = "Baicells"
    '''
    fatedges = [
        {
            'Name': 'Beijing',
            'SN': 'Unknown',
            'IP': 'Unknown',
            'NetworkModel': 'Unknown',
            'Online': 'OFF',
            'SPEC': 'Unknown',
            'SW': 'Unknown',
            'ThinEdges': [
                {
                    'Name': 'Nanjing',
                    'SN': 'Unknown',
                    'IP': 'Unknown',
                    'Online': 'OFF',
                    'SPEC': 'Unknown',
                    'SW': 'Unknown',
                    'Tunnels': 'Unknown'
                },
                {
                    'Name': 'Shenzhen',
                    'SN': 'Unknown',
                    'IP': 'Unknown',
                    'Online': 'OFF',
                    'SPEC': 'Unknown',
                    'SW': 'Unknown',
                    'Tunnels': 'Unknown'
                },
                {
                    'Name': 'AliCloud',
                    'SN': 'Unknown',
                    'IP': 'Unknown',
                    'Online': 'OFF',
                    'SPEC': 'Unknown',
                    'SW': 'Unknown',
                    'Tunnels': 'Unknown'
                },
            ]
        },
    ]
    '''
    fatedges = Singleton.getInstance().fatedges()
    return render_template("overview.html", region=region, fatedges=fatedges)

@app.route("/todo")
@app.route("/todo/")
def todo():
    return render_template("todo.html")

@app.route("/north/", methods=("POST", ))
def north():
    cmd = request.form["CMD"]
    if cmd == "poll":
        SN = request.form["SN"]
        return Singleton.getInstance().getresponse(SN)
    elif cmd == "query":
        print("query command")
        try:
            SN = request.form["sn"]
            return (Singleton.getInstance().queryCMD(SN, request.form))
        except Exception as e:
            print("log")
            print(e)
        return "Query OK"
    else:
        return "Unknown"


if __name__ == "__main__":
    Singleton.getInstance()
    app.run()
