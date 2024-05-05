from flask import Flask, render_template, request, redirect, send_file

# Flask 애플리케이션을 생성합니다.
app = Flask("JobScraper")

# 홈 페이지를 위한 route를 정의합니다.


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    return render_template("search.html", keyword=keyword)


# Flask 애플리케이션을 실행합니다.
app.run("0.0.0.0")
