from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.remote import extract_remote_jobs
from file import save_to_file

# Flask 애플리케이션을 생성합니다.
app = Flask("JobScraper")

# 홈 페이지를 위한 route를 정의합니다.


@app.route("/")
def home():
    return render_template("home.html")


# db 딕셔너리 추가(이미 이전에 검색한 결과를 또 리로드하지 않고 바로 db 딕셔너리에서 찾을 수 있게)
db = {}

# 검색 페이지 라우터


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        # 키워드가 지정되지 않은 경우 홈 페이지로 리디렉션합니다.
        return redirect("/")
    if keyword in db:
        # 이미 검색된 키워드의 결과가 있는 경우, 데이터베이스에서 결과를 가져옵니다.
        jobs = db[keyword]
    else:
        # 새로운 키워드에 대한 검색을 실행하고 결과를 데이터베이스에 저장합니다.
        wwr = extract_wwr_jobs(keyword)
        remote = extract_remote_jobs(keyword)
        jobs = wwr + remote
        db[keyword] = jobs
        # 검색 결과를 템플릿으로 렌더링하여 사용자에게 표시합니다.
    return render_template("search.html", keyword=keyword, jobs=jobs)

# 파일 추출 페이지 라우터


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


# Flask 애플리케이션을 실행한다.
app.run("0.0.0.0")
