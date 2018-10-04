import analyzer
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/<int:count>/")
def output(count):
	name = "Natalie";
	topWord = analyzer.getXTopNgrams("9/22/2018  5:53:11 AM","10/3/2018  11:53:11 PM", count, 2)
	return render_template('charts.html', name = name, faveWord = topWord)



if __name__ == "__main__":
	app.run(debug = True)