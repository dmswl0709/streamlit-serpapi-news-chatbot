import streamlit as st
import requests
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re

# SerpApi API 키
SERP_API_KEY = "e76e7a8edcbd6eab9f9fc31e72567b8351570da93115bfeb93abca39d2153909"

# 한글 폰트 설정
def set_korean_font():
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"  # macOS AppleGothic 폰트 경로
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())  # 그래프에 폰트 적용
    plt.rc('axes', unicode_minus=False)  # 마이너스 기호가 깨지는 문제 방지

def fetch_google_news(query, api_key, date_range, language, region):
    tbs_mapping = {
        "전체": "",
        "최근 일주일": "qdr:w",
        "최근 한 달": "qdr:m",
        "최근 1년": "qdr:y"
    }
    params = {
        "q": query,
        "tbm": "nws",
        "api_key": api_key,
        "hl": language,
        "gl": region,
        "tbs": tbs_mapping[date_range]
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        data = response.json()
        if "news_results" in data:
            return data["news_results"]
        else:
            st.error("SerpApi 응답에 'news_results' 필드가 없습니다.")
            return []
    else:
        st.error(f"API 요청 실패. 상태 코드: {response.status_code}")
        return []

def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # 특수문자 제거
    text = text.lower()  # 소문자로 변환
    stop_words = {"the", "and", "is", "to", "in", "for", "of", "a", "on", "with", "by"}
    words = [word for word in text.split() if word not in stop_words]
    return words

def plot_keyword_frequency(news_data):
    set_korean_font()  # 한글 폰트 설정
    combined_text = " ".join(
        article["title"] + " " + article.get("snippet", "") for article in news_data
    )
    words = preprocess_text(combined_text)
    word_counts = Counter(words).most_common(10)

    if word_counts:
        words, counts = zip(*word_counts)
        plt.figure(figsize=(10, 6))
        plt.bar(words, counts, color="skyblue")
        plt.xlabel("키워드")
        plt.ylabel("빈도수")
        plt.title("뉴스 키워드 빈도 분석")
        st.pyplot(plt)
    else:
        st.write("분석할 키워드 데이터가 없습니다.")

# Streamlit UI
st.title("Google AI 뉴스 요약 챗봇")
st.write("이 앱은 SerpApi와 Streamlit을 사용해 Google AI 관련 뉴스를 검색하고 요약합니다.")

query = st.text_input("검색어를 입력하세요:", value="Google AI")
st.sidebar.title("검색 필터")
date_range = st.sidebar.selectbox("날짜 범위", ["전체", "최근 일주일", "최근 한 달", "최근 1년"])
language = st.sidebar.text_input("언어 코드 (예: en, ko):", value="en")
region = st.sidebar.text_input("지역 코드 (예: us, kr):", value="us")

if st.button("뉴스 검색"):
    st.write("뉴스를 검색 중입니다...")
    news = fetch_google_news(query, SERP_API_KEY, date_range, language, region)
    if not news:
        st.error("뉴스를 찾을 수 없습니다.")
    else:
        st.session_state["news"] = news
        st.write("검색된 뉴스:")
        for idx, article in enumerate(news[:5]):
            st.subheader(f"{idx + 1}. {article['title']}")
            st.write(article.get("snippet", ""))
            st.markdown(f"[기사 읽기]({article['link']})")

if st.button("키워드 분석"):
    if "news" not in st.session_state or not st.session_state["news"]:
        st.error("키워드 분석을 위해 먼저 뉴스를 검색하세요.")
    else:
        st.write("뉴스 키워드 빈도 분석 결과:")
        plot_keyword_frequency(st.session_state["news"])