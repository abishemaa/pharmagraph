from flask import Flask, render_template, jsonify
from core.engine import get_all_drugs, get_network_stats, init as engine_init

app = Flask(__name__, template_folder='interface/flask/templates')

# Initialize the core engine (load and enrich graph) so endpoints return data
engine_init()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/all')
def all_drugs():
    return render_template('all_drugs.html', drugs=get_all_drugs())

@app.route('/drug/<name>')
def drug_info(name):
    return

@app.route('/stats')
def stats():
    return render_template('stats.html', stats=get_network_stats())

@app.route('/explain/<d1>/<d2>')
def explain_interaction(d1, d2):
    return

@app.route('/path/<d1>/<d2>')
def interaction_path(d1, d2):
    return

@app.route('/graph')
def graph():
    return

@app.route('/subgraph/graph')
def subgraph():
    return



app.run(debug=True)