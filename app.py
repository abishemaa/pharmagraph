from flask import Flask, render_template

app = Flask(__name__, template_folder='interface/flask/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/visualizer')
def visualizer():
    return "This is the visualizer page."    



app.run(debug=True)