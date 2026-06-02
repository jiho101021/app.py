import streamlit as st
from xai_sdk import Client
from xai_sdk.chat import user, system
import os

# 페이지 설정
st.set_page_config(
    page_title="⚽ Soccer Star AI",
    page_icon="⚽",
    layout="centered"
)

st.title("⚽ Soccer Star AI")
st.caption("축구 선수의 커리어, 득점, 어시스트, 국적 등을 물어보세요!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    try:
        api_key = st.secrets["XAI_API_KEY"]
        st.session_state.client = Client(api_key=api_key)
    except Exception as e:
        st.error("API 키를 불러올 수 없습니다. Streamlit Secrets에 XAI_API_KEY를 추가해주세요.")
        st.stop()

# 이전 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 시스템 프롬프트 (축구 전문가 역할)
system_prompt = """You are a professional soccer analyst with deep knowledge of football history.
You provide accurate information about players' careers, goals, assists, nationality, clubs, achievements, and statistics.
Always answer in Korean. Be friendly and enthusiastic about football."""

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요... (예: 메시의 통산 골 기록은?)"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("Grok이 생각 중... ⚽"):
            try:
                chat = st.session_state.client.chat.create(model="grok-4.3")  # 현재 가장 좋은 모델
                
                # 시스템 프롬프트 + 이전 대화 기록
                chat.append(system(system_prompt))
                
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        chat.append(user(msg["content"]))
                    elif msg["role"] == "assistant":
                        chat.append({"role": "assistant", "content": msg["content"]})  # 이전 응답도 추가

                response = chat.sample()
                answer = response.content
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = f"오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
