# https://remoteok.com/ 사이트 직업 정보를 추출하는 코드

from bs4 import BeautifulSoup
import requests


def extract_remote_jobs(keyword):
    # 검색어를 이용하여 직업 정보를 제공하는 웹페이지의 URL 저장
    base_url = f"https://remoteok.com/remote-{keyword}-jobs"

    # HTTP GET 요청을 보내고 응답을 받음
    request = requests.get(base_url, headers={"User-Agent": "Juni"})

    '''
    User-Agent 헤더는 웹 서버에 요청을 보낸 클라이언트(사용자 에이전트)를 나타내는 문자열입니다. 
    웹 서버는 User-Agent 헤더를 통해 어떤 브라우저나 클라이언트 소프트웨어가 요청을 보냈는지 식별할 수 있습니다.
      "Juni"라는 문자열은 임의로 선택된 사용자 에이전트를 나타냅니다.
    '''

    # HTTP 요청에 실패했을 경우 에러 프린트
    if request.status_code != 200:
        print("Can't request website")
    else:   # HTTP 요청에 성공했을 경우
        # 추출된 결과를 저장할 리스트 초기화
        results = []
        # BeautifulSoup을 사용하여 HTML을 파싱함.
        soup = BeautifulSoup(request.text, "html.parser")
        # 각 직업 정보가 포함된 테이블 행(tr) 요소를 찾는다.
        jobs = soup.find_all("tr", class_="job")
        # 각 직업 정보에 대해 반복
        for job in jobs:
            # 링크 추출
            link = job.find("a", itemprop="url")
            # 회사 이름을 추출
            company = job.find("h3", itemprop="name")
            # 직무 제목을 추출
            position = job.find("h2", itemprop="title")
            # 위치(지역), 월급 정보를 추출
            locations = job.find_all("div", class_="location")
            location = locations[0]
            salary = locations[-1]
            # 추출한 정보를 다듬으면서 공백을 제거하고 문자열로 변환
            if company:
                company = company.string.strip()
            if position:
                position = position.string.strip()
            if location:
                location = location.string.strip()
            if salary:
                salary = salary.string.strip()
            # 회사 이름, 직무 제목, 위치 정보가 모두 존재할 경우
            if company and position and location:
                # 추출한 정보를 딕셔너리 형태로 저장
                job_data = {
                    'link': f"https://remoteok.com{link['href']}",
                    'company': company,
                    'title': position,
                    'location': location,
                    'note': salary,
                }
                # 결과 리스트에 딕셔너리 추가
                results.append(job_data)

    # 추출된 모든 결과를 반환
    return results
