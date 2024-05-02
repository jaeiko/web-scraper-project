from flask import Flask, render_template, request, redirect, send_file

app = Flask("JobScrapper")


@app.route("/")
def home():
    return "Hello World!"


app.run("0.0.0.0")
