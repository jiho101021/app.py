import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="⚽ Soccer Star AI",
    page_icon="⚽",
    layout="centered"
)

st.title("⚽ Soccer Star AI")
st.caption("축구 선수의 커리어, 득점, 어시스트, 국적 등을 물어보세요!")

# 세션 상태
if "messages" not in st.session_state:
    st.session_state.messages = []

# OpenAI 클라이언트 (xAI)
if "client" not in st.session_state:
    try:
        api_key = st.secrets["XAI_API_KEY"]
        st.session_state.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
    except Exception as e:
        st.error("❌ Secrets에서 XAI_API_KEY를 찾을 수 없습니다.")
        st.stop()

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_prompt = """당신은 세계 최고의 축구 전문가입니다. 
선수의 국적, 커리어, 클럽 경력, 득점 기록, 어시스트, 수상 경력 등을 정확하게 알려주세요.
항상 한국어로 친근하게 답변합니다."""

if prompt := st.chat_input("선수 이름을 입력하세요. 예: 메시 통산골, 호날두 국적..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Grok이 분석중입니다... ⚽"):
            try:
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
                
            except Exception as e:
                st.error(f"오류: {str(e)}")
