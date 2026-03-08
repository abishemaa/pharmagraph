#app.py
from flask import Flask, render_template, request, jsonify
from graph.api import graph_to_json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/graph")
def graph():
    drug = request.args.get("drug")
    data = graph_to_json(drug if drug else None)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)