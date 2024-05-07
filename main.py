from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.remote import extract_remote_jobs

# Flask 애플리케이션을 생성합니다.
app = Flask("JobScraper")

# 홈 페이지를 위한 route를 정의합니다.


@app.route("/")
def home():
    return render_template("home.html")


db = {}


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        wwr = extract_wwr_jobs(keyword)
        remote = extract_remote_jobs(keyword)
        jobs = wwr + remote
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


# Flask 애플리케이션을 실행합니다.
app.run("0.0.0.0")
