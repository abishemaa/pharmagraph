from flask import Flask, render_template, jsonify, request
from database import get_all_drugs, get_all_interactions
from loader import load_data
from database import setup_database

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/graph")
def graph():

    drug = request.args.get("drug", "").lower()

    nodes = []
    links = []

    # create nodes
    seen = set()

    for name, cls, moa, met in get_all_drugs():

        if name in seen:
            continue

        seen.add(name)

        nodes.append({
            "id": name,
            "class": cls or "",
            "moa": moa or "",
            "metabolism": met or ""
        })
    # create links
    for d1, d2, severity in get_all_interactions():

        if drug and drug not in (d1.lower(), d2.lower()):
            continue

        links.append({
            "source": d1,
            "target": d2,
            "severity": severity
        })

    return jsonify({
        "nodes": nodes,
        "links": links
    })


if __name__ == "__main__":

    setup_database()
    load_data()

    app.run(debug=True)