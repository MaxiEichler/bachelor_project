from flask import Flask, render_template, request, jsonify
from logic.GUI_connection import process_coordinates
from logic.Routing import set_path, unblock_last_connection, unblock_all_connections
from hardware.ASA import set_ASA
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

def log(message):
    print(f"{datetime.now().strftime('%M:%S.%f')[:-3]} - {message}")

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

# Receive data from server 
@app.route("/send-coordinates", methods=["POST"])
def receive_coordinates():
    #log("Start of transmission")
    data = request.json  # receive JSON from JS
    
    x1 = data.get("x1")
    x2 = data.get("x2")
    routetype = data.get("routeType")

    result = process_coordinates(x1, x2)
    #print("processed coordinates: ", result[0], result[1])
    set_path(result[0], result[1], routetype)  # Call set_path with the processed coordinates
    #print("result: ",result)
    return jsonify({"result": result})

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route("/remove-route", methods=["POST"])
def receive_removed_route():
    data = request.json
    unblock_last_connection() 
    return jsonify({})

#/////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route("/remove-all", methods=["POST"])
def receive_removed_all():
    data = request.json
    unblock_all_connections()
    return jsonify({})
