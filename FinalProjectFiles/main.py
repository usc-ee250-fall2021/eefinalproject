from flask import Flask, redirect, url_for, request, session
from flask import render_template
import data

app = Flask(__name__)



@app.route("/") #methods=["GET","POST"]
def home():
    return render_template("index.html", pearson = 0, spearman = 0, kendall=0)

@app.route('/search', methods=['GET', 'POST'])
def search():
    state = request.args['state']
    ticker = request.args['ticker']
    correlations = data.datamain(state, ticker)
    graph = data.getGraph(ticker, state)
    return render_template("index.html", statetext = state, tickertext=ticker, pearson = correlations[0], spearman = correlations[1], kendall=correlations[2], graphimage = graph)

if __name__ == "__main__":
    app.debug=True
    app.run()
    
