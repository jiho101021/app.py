import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="⚽ Soccer Star AI",
    page_icon="⚽",
    layout="centered"
)

st.title("⚽ Soccer Star AI")
st.caption("축구 선수의 커리어, 득점, 어시스트, 국적 정보를 알려드려요!")

# Secrets에서 API 키 불러오기
if "gemini_configured" not in st.session_state:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        st.session_state.gemini_configured = True
    except Exception as e:
        st.error("❌ Secrets에 GEMINI_API_KEY를 추가해주세요.")
        st.stop()

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 시스템 프롬프트
system_prompt = """당신은 세계 최고의 축구 전문 분석가입니다.
축구 선수의 국적, 클럽 커리어, 총 득점, 어시스트, 주요 기록, 수상 경력 등을 정확하고 자세하게 알려주세요.
항상 한국어로 친근하고 열정적으로 답변하세요."""

# 사용자 입력
if prompt := st.chat_input("선수 이름을 입력하세요 (예: 손흥민, 메시, 호날두 통산 골)"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("Gemini가 분석중입니다... ⚽"):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash-lite",
                    system_instruction=system_prompt
                )
                
                # 대화 기록을 포함한 메시지 생성
                chat_history = []
                for msg in st.session_state.messages:
                    chat_history.append({"role": msg["role"], "parts": [msg["content"]]})
                
                response = model.generate_content(chat_history)
                answer = response.text
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                error_msg = f"오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
