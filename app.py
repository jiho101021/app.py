import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="⚽ Soccer Star AI", page_icon="⚽", layout="centered")

st.title("⚽ Soccer Star AI")
st.caption("축구 선수 커리어 · 골 · 어시스트 정보 챗봇")

# API 클라이언트 초기화
if "client" not in st.session_state:
    try:
        api_key = st.secrets["XAI_API_KEY"]
        st.session_state.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
    except Exception as e:
        st.error("❌ Secrets에 XAI_API_KEY를 추가해주세요.")
        st.stop()

# 대화 기록
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_prompt = """당신은 최고의 축구 전문가입니다. 
선수의 국적, 커리어, 득점 기록, 어시스트, 수상 이력 등을 정확하게 알려주세요. 
한국어로 친근하게 답변하세요."""

if prompt := st.chat_input("예: 손흥민 프리미어리그 골 기록은?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Grok이 분석중... ⚽"):
            response = st.session_state.client.chat.completions.create(
                model="grok-4.3",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                temperature=0.7,
                max_tokens=2048
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
