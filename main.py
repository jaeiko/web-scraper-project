from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.remote import extract_remote_jobs
from extractors.saramin import extract_saramin_jobs
from file import save_to_file

# Flask 애플리케이션을 생성
app = Flask("JobScraper")


@app.route("/")  # 홈 페이지를 위한 route를 정의
def home():
    return render_template("home.html")

# 500 에러 핸들러


@app.errorhandler(500)
def internal_server_error(e):
    # 사용자에게 표시할 메시지
    error_message = "죄송합니다. 서버에서 오류가 발생했습니다. 문제가 지속되면 관리자에게 문의해주세요."
    # 오류 페이지에 렌더링할 템플릿 또는 메시지 반환
    return render_template("error.html", error_message=error_message), 500


# db 딕셔너리 추가(이미 이전에 검색한 결과를 또 리로드하지 않고 바로 db 딕셔너리에서 찾을 수 있게)
db = {}


@app.route("/search")   # 검색 페이지 라우터
def search():
    keyword = request.args.get("keyword")   # 키워드 입력 받음

    wwr = extract_wwr_jobs(keyword)
    remote = extract_remote_jobs(keyword)
    saramin = extract_saramin_jobs(keyword)
    jobs = wwr + remote + saramin
    db[keyword] = jobs
    # 검색 결과를 템플릿으로 렌더링하여 사용자에게 표시합니다.
    return render_template("search.html", keyword=keyword, wwr=wwr, remote=remote, saramin=saramin, jobs=jobs)


@app.route("/export")   # 파일 추출 페이지 라우터
def export():
    keyword = request.args.get("keyword")
    if keyword == None:  # 해당 keyword가 비워져 있으면 다시 홈으로 리다이렉트
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


# Flask 애플리케이션을 실행
app.run("0.0.0.0")
