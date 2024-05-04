from flask import Flask, render_template, request, redirect, send_file

# Flask 애플리케이션을 생성합니다.
app = Flask("__main__")

# 홈 페이지를 위한 route를 정의합니다.
@app.route("/")
def home():
    return render_template("home.html")

# Flask 애플리케이션을 실행합니다.
app.run("0.0.0.0")