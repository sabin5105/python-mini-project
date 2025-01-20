#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###############################################################################
# (1) APA 레퍼런스에서 '제목'만 추출하는 함수
###############################################################################
def extract_title_from_apa(apa_line: str) -> str:
    """
    아주 단순화된 방식으로 APA 참고문헌에서 '제목'만 추출.
    예) "Zhang, R., Zou, D., & Cheng, G. (2024). A review of chatbot-assisted learning...
          Interactive Learning Environments, 32(8), 4529-4557."
    """

    # 1) "저자 (~). 연도. 제목. 저널, 볼륨(호), 페이지..." 형태에서,
    #    연도 뒤의 텍스트(=제목+저널+기타)만 우선 추출
    main_pattern = re.compile(r'^(.*?)\s*\(\d{4}\)\.\s*(.*)$')
    m = main_pattern.search(apa_line.strip())
    if not m:
        return ""  # 실패 시 빈 문자열 반환

    rest = m.group(2).strip()

    # 2) 위에서 얻은 문자열에서 '마침표(".") + 공백'까지를 '제목'으로 간주
    #    예) "A review of chatbot-assisted learning... Interactive Learning... -> A review of chatbot-assisted learning..."
    title_pattern = re.compile(r'^(.*?)\.\s+(.*)$')
    t = title_pattern.search(rest)
    if t:
        return t.group(1).strip()
    else:
        # 마침표(".")가 없다면 전체를 제목으로 처리
        return rest


###############################################################################
# (2) Selenium 통해 Google Scholar에서 BibTeX 가져오기
###############################################################################
def get_bibtex_from_google_scholar(title: str, driver: webdriver.Chrome) -> str:
    """
    Selenium을 사용하여 Google Scholar에 접속해 title을 검색하고,
    첫 번째 결과의 'Cite(인용)' -> 'BibTeX' 버튼을 클릭하여 나온 텍스트를 반환.
    
    검색 실패/오류 시에는 빈 문자열 리턴.
    """
    if not title:
        return ""

    try:
        # 1) 구글 스칼라 메인 페이지 열기
        driver.get("https://scholar.google.com/")

        # 2) 검색창에 title 입력 후 Enter
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(title)
        search_box.send_keys(Keys.RETURN)

        # 3) 첫 번째 결과의 "인용" 버튼 클릭
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gs_ri"))
        )
        cite_button = driver.find_element(By.CSS_SELECTOR, ".gs_ri .gs_or_cit.gs_nph")
        cite_button.click()

        # 4) "BibTeX" 링크 클릭
        bibtex_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "BibTeX"))
        )
        bibtex_link.click()

        # 5) BibTeX 텍스트 추출
        pre_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        return pre_tag.text.strip()

    except Exception as e:
        print(f"[ERROR] '{title}' 검색/인용/BibTeX 추출 중 오류 발생: {e}")
        return ""


###############################################################################
# (3) APA 문자열 -> 제목 추출 -> 구글 스칼라 검색 -> BibTeX 추출
###############################################################################
def convert_apa_to_bibtex_using_selenium(apa_line: str, driver: webdriver.Chrome) -> str:
    """
    APA 레퍼런스 한 줄 -> '제목'만 추출 -> 구글 스칼라 검색 -> BibTeX 추출
    """
    # 1) APA 문자열에서 제목 추출
    title = extract_title_from_apa(apa_line)
    if not title:
        return f"% Failed to parse title from: {apa_line}"

    # 2) Google Scholar에서 BibTeX 가져오기
    bibtex_str = get_bibtex_from_google_scholar(title, driver)
    if not bibtex_str:
        return f"% Google Scholar search failed or no BibTeX found for: {title}"

    return bibtex_str


###############################################################################
# (4) 메인 함수
###############################################################################
def main(apa_input_file="apa_input.txt", bibtex_output_file="bibtex_output.txt", headless=False):
    """
    1) apa_input_file 에서 각 줄(APA 레퍼런스)을 읽음
    2) convert_apa_to_bibtex_using_selenium() 실행
    3) bibtex_output_file 에 결과 저장

    :param apa_input_file: APA 참고문헌이 라인 별로 저장된 텍스트 파일
    :param bibtex_output_file: 변환된 BibTeX를 저장할 파일
    :param headless: 브라우저 창을 띄우지 않는 headless 모드 사용 여부
    """
    # (옵션) 브라우저 창을 띄우지 않는 headless 모드 등 설정
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")

    # 크롬 드라이버 실행 (특정 경로 지정이 필요하면 직접 명시)
    driver = webdriver.Chrome(options=options)

    try:
        with open(apa_input_file, 'r', encoding='utf-8') as f_in, \
             open(bibtex_output_file, 'w', encoding='utf-8') as f_out:

            for line in f_in:
                line = line.strip()
                if not line:
                    continue  # 빈 줄은 스킵

                # APA -> BibTeX 변환
                bibtex_entry = convert_apa_to_bibtex_using_selenium(line, driver)
                f_out.write(bibtex_entry + "\n\n")

                # 너무 빠른 연속 요청은 Google Scholar에서 CAPTCHA가 뜰 수 있으므로 적절히 대기
                time.sleep(3)
    finally:
        driver.quit()

    print(f"[INFO] 변환 완료! 결과 파일: '{bibtex_output_file}'")


###############################################################################
# (5) 스크립트 진입점
###############################################################################
if __name__ == "__main__":
    # ex) python apa_to_bibtex.py input.txt output.txt --headless
    #     python apa_to_bibtex.py input.txt output.txt
    #     python apa_to_bibtex.py  (기본값: apa_input.txt -> bibtex_output.txt)
    cli_args = sys.argv[1:]

    apa_input_file = "apa_input.txt"
    bibtex_output_file = "bibtex_output.txt"
    headless_mode = False

    # 간단한 파싱(옵션에 따라 직접 argparse 사용 가능)
    if len(cli_args) >= 1:
        apa_input_file = cli_args[0]
    if len(cli_args) >= 2:
        bibtex_output_file = cli_args[1]
    if "--headless" in cli_args:
        headless_mode = True

    main(apa_input_file, bibtex_output_file, headless=headless_mode)