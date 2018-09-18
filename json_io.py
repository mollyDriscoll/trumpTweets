import analyzer
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/output")
def output():
	return render_template('charts.html', random = 30)



if __name__ == "__main__":
	app.run(debug = True)