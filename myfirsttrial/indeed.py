import requests
from bs4 import BeautifulSoup
# html에서 정보를 추출하기위한 모듈
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 궁금한건 이페이지에서 찾아보기

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    # indeed사이트에서 python 검색하는 url입력
    # print(resul)  
    # print(resul.text)  
    soup = BeautifulSoup(result.text, "html.parser")
    # html코드 파싱

    pagination = soup.find("div", {"class": "pagination"})
    # F12눌러서 페이지의 숫자있는 html찾기
    links = pagination.find_all('a')
    # 페이지의 숫자있는 html찾기

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
        # 페이지 몇까지있는지 반복문돌려 리스트에 넣기
    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    # 강의는 div라 하지만 홈페이지는 div에서 h2로 코드변경
    # 회사업무 출력
    company = html.find("span", {"class": "company"})
    # print(company)
    # 각 회사에 링크가있는게 있고 없는게있다

    if company:
      company_anchor = company.find('a')

      if company_anchor is not None:
          company = str(company_anchor.string)
          # 회사링크가 있다면 anchor의 string출력
      else:
          company = str(company.string)
          # 회사링크가 없다면 span의 string출력
      company = company.strip()
    else:
      company = None
    # 공백제거
    # location = html.find('span', {'class': 'location'}) - 불가
    # 회사 주소추출
    # 재택근무가있을수도 있으니 주소없을 가능성있다
    # span말고 div에 display:none가 있다 그리고 location도 있다
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    # 뭔지는 모르겠지만 data-rc-loc 에 회사주소가 담겨있다 추출가능
    # print(location)
    # 정상적으로 주소가 출력된다

    # 각 업무를 누르면 회사모집 페이지로 들어가짐
    # 누르면 URL이 이동되고 연결되는 id가 URL에 표시된다
    # id넘버까지 남겨두고 쓸모없는 것을 지우고 다시 확인했을때
    # 정상출력이된다면 그 id넘버를 html에서 찾는다
    job_id = html['data-jk']
    # extract_indeed_jobs에 있는 변수 results에서
    # 아까 확인했던 URL의 id를 찾을수 있는 것은 data-jk이다
    return {'title': title,
            'company': company,
            'location': location,
            'link': f'https://www.indeed.com/viewjob?jk={job_id}'}
    # 회사업무와 회사명칭, 주소, 회사모집페이지 리턴


# 페이지가 넘어갈수록 url은 변함
# 첫 페이지 url: https://www.indeed.com/jobs?q=python&limit=50
# 마지막 페이지 url: https://www.indeed.com/jobs?q=python&limit=50&start=950
# 각 페이지 일자리정보 추출 리스트에 담고 모든일자리를 반환
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeed page {page}")
        # 총20페이지 페이지 전부 반복하는지 확인작업
        result = requests.get(f'{URL}&start={page*LIMIT}')
        # 페이지 요청

        # print(result.status_code)
        # 정상적으로 요청되는지 확인 200이 20번 나오면 성공
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
        # F12눌러서 페이지의 일자리 링크 html찾기

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
  last_page = get_last_page() 
  
  jobs = extract_jobs(last_page)
  return jobs
   # 이 함수는 지금 indeed.py 안에 넣놓고 불필요한 이름 바꿔 준거임 
