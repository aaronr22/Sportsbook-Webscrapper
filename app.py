from flask import Flask, render_template, request, Markup
import os
import pipeline

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            results = pipeline.run_pipeline()
        except Exception as e:
            print(e)
            errors.append("Could not run pipeline")
    return render_template('index.html', errors=errors, results=Markup(results))

if __name__ == '__main__':
    app.run()