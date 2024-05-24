# 출력 결과를 csv 파일로 저장하는 함수
def save_to_file(file_name, jobs):
    # ‘파일 이름’과 ‘파일 열기 모드’를 입력값으로 받고 결괏값으로 파일 객체를 리턴
    file = open(f"{file_name}.csv", "w", encoding="utf-8-sig")

    # 문자열 데이터를 파일에 직접 쓰자.
    file.write("Position, Company, Location, URL\n")

    # 파일에 position, company, location, link 열로 해서 데이터 저장한다.
    for job in jobs:
        file.write(
            f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n"
        )

    file.close()
