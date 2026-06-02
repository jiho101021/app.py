import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="⚽ Soccer Star AI", page_icon="⚽", layout="centered")

st.title("⚽ Soccer Star AI")
st.caption("축구 선수 커리어, 골, 어시스트, 국적 챗봇")

# API 키 설정
if "configured" not in st.session_state:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        st.session_state.configured = True
    except:
        st.error("❌ Secrets에 GEMINI_API_KEY를 추가해주세요!")
        st.stop()

# 대화 기록
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

system_prompt = """당신은 최고의 축구 전문가입니다. 
선수의 국적, 커리어, 득점, 어시스트, 수상 경력 등을 정확하고 자세히 알려주세요. 
한국어로 친근하게 답변하세요."""

if prompt := st.chat_input("예: 손흥민 총 골 기록은?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini 분석중... ⚽"):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=system_prompt
                )
                
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]} 
                    for m in st.session_state.messages[:-1]
                ])
                
                response = chat.send_message(prompt)
                answer = response.text
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"오류: {str(e)}")
