from flask import Flask
app = Flask("JobScrapper")


@app.route('/')
def hello():
    return 'Hello, World!'


app.run("0.0.0.0")
