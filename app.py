import streamlit as st
import requests

# SerpApi API 키
SERP_API_KEY = "e76e7a8edcbd6eab9f9fc31e72567b8351570da93115bfeb93abca39d2153909"

def fetch_google_news(query, api_key, date_range, language, region):
    # 날짜 필터 매핑
    tbs_mapping = {
        "전체": "",
        "최근 일주일": "qdr:w",
        "최근 한 달": "qdr:m",
        "최근 1년": "qdr:y"
    }
    params = {
        "q": query,
        "tbm": "nws",  # 뉴스 검색 모드
        "api_key": api_key,
        "hl": language,  # 언어 설정
        "gl": region,    # 지역 설정
        "tbs": tbs_mapping[date_range]  # 날짜 필터
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        return response.json().get("news_results", [])
    else:
        st.error(f"Error: {response.status_code}")
        return []

st.title("Google AI 뉴스 요약 챗봇")
st.write("이 앱은 SerpApi와 Streamlit을 사용해 Google AI 관련 뉴스를 검색하고 요약합니다.")

# 검색어 입력
query = st.text_input("검색어를 입력하세요:", value="Google AI")

# 검색 필터링 UI 추가
st.sidebar.title("검색 필터")
date_range = st.sidebar.selectbox("날짜 범위", ["전체", "최근 일주일", "최근 한 달", "최근 1년"])
language = st.sidebar.text_input("언어 코드 (예: en, ko):", value="en")
region = st.sidebar.text_input("지역 코드 (예: us, kr):", value="us")

# 뉴스 검색 버튼
if st.button("뉴스 검색"):
    st.write("뉴스를 검색 중입니다...")
    news = fetch_google_news(query, SERP_API_KEY, date_range, language, region)
    
    if not news:
        st.error("뉴스를 찾을 수 없습니다.")
    else:
        for idx, article in enumerate(news[:5]):  # 최대 5개의 뉴스 표시
            st.subheader(f"{idx + 1}. {article['title']}")
            st.write(article.get("snippet", ""))
            st.markdown(f"[기사 읽기]({article['link']})")