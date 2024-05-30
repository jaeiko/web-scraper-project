# https://weworkremotely.com/ 사이트 직업 정보를 추출하는 코드

from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    # 검색어를 이용하여 직업 정보를 제공하는 웹페이지의 URL 저장
    base_url = "https://weworkremotely.com/remote-jobs/search?&term="

    # HTTP GET 요청을 보내고 응답을 받음
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website")
    else:
        # 추출된 결과를 저장할 리스트 초기화
        results = []
        # BeautifulSoup을 사용하여 HTML을 파싱
        soup = BeautifulSoup(response.text, "html.parser")
        # 각 직업 정보가 포함된 요소를 찾음
        jobs = soup.find_all("section", class_="jobs")
        # 각 직업 정보에 대해 반복
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                # 링크 추출
                link = anchor['href']
                # 회사, 종류, 지역 정보를 추출
                company, kind, region = anchor.find_all(
                    'span', class_="company")
                title = anchor.find('span', class_="title")
                # 추출한 정보를 딕셔너리 형태로 저장
                job_data = {
                    'link': f"https://weworkremotely.com/{link}",
                    'company': company.string.replace(",", " "),
                    'location': region.string.replace(",", " "),
                    'title': title.string.replace(",", " "),
                    "note": kind.string.replace(",", " "),
                }
                # 결과 리스트에 딕셔너리 추가
                results.append(job_data)

    # 추출된 모든 결과를 반환
    return results
