import sys
print(sys.path)
from controllerv2.core import Singleton

from flask import render_template
from flask import Flask, request
import sys
import json
import os

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
    elif cmd == "actionresult":
        actionID = request.form["actionID"]
        result = request.form["result"]
        Singleton.getInstance().actionresult(actionID, result)
        return "OK"
    else:
        return "Unknown"

@app.route("/north/actionresult/", methods=("POST",))
def actionresult():
    try:
        actiontype = request.form["actiontype"]
        actionid = request.form["actionid"]
        sn = request.form["sn"]
        returncode = request.form["returncode"]
        #astderr = request.form["stderr"]
    except Exception as e:
        print(request.form)
        print("Exception: ", e)
        print("Invalid actionresult report from edge")
        return "NOK"



    if actiontype == "query":
#        print(request.form)
#        print(request.form["stdout"])
        if returncode != "0":
            print(request.form)
            print("Error action report")
            return "NOK"
        astdout = json.loads(request.form["stdout"].replace("'", '"'))
        Singleton.getInstance().queryCMD2(sn, astdout)
    elif actiontype == "tunnel":
        if returncode == "0":
            print("actionresult", request.form["stdout"], actionid)
            Singleton.getInstance().actionresult(actionid, request.form["stdout"])
        else:
            Singleton.getInstance().actionresult(actionid, request.form["stderr"])
        pass
    else:
        print("unknown actiontype", actiontype)


    return "OK"



@app.route("/procedureorchestration")
def procedureorchestration():
    fatedges = Singleton.getInstance().fatedges()
    thinedges = Singleton.getInstance().thinedges()
    return render_template("procedure-ochecstration.html", fatedges=fatedges, thinedges=thinedges)

@app.route("/orchestration")
def orchestration():
    tunnels = Singleton.getInstance().tunnels()

    return render_template("orchestration.html", tunnels = tunnels)


@app.route("/newtunnel.html", methods=("POST", ))
def newtunnel():
    result = Singleton.getInstance().newtunnel(request.form)

    if result == "OK":
        return redirecturl()
    else:
        return render_template("status.html", result = result)



@app.route("/deletetnl.html", methods=("POST", ))
def deletetnl():
    tunnels = Singleton.getInstance().deletetnl(request.form)
    return redirecturl()

def redirecturl():
    return '<html><head> ' \
    '<meta http-equiv="refresh" content="0; url=/orchestration" /> ' \
    '</head><body></body>' \
    '</html>'

@app.route("/actions")
def actions():
    return render_template("actions.html", acts = Singleton.getInstance().actions())

def runningUnderGitProjectRootDirectory(cwd):
    return os.path.isdir(os.path.join(cwd, "controllerv2"))

if __name__ == "__main__":
    print("Checking working directory ...")
    cwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(cwd)
    assert runningUnderGitProjectRootDirectory(cwd)
    os.chdir(cwd + "/controllerv2")

    Singleton.getInstance()
    app.run(host="0.0.0.0", port=8080)

