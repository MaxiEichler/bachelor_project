from flask import Flask, render_template, request, jsonify
from logic.GUI_connection import process_coordinates
from logic.Routing import set_path

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Receive data from server 
@app.route("/send-coordinates", methods=["POST"])
def receive_coordinates():
    data = request.json  # receive JSON from JS

    x1 = data.get("x1")
    y1 = data.get("y1")
    x2 = data.get("x2")
    y2 = data.get("y2")

    # Call function from main.py
    result = process_coordinates(x1, y1, x2, y2)
    set_path(result[0], result[1])  # Call set_path with the processed coordinates
    print("result: ",result)
    return jsonify({"result": result})
