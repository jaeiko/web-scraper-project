from flask import Flask, render_template, request, redirect, send_file

app = Flask("__main__")


@app.route("/")
def home():
    return render_template("home.html")


app.run("0.0.0.0")
