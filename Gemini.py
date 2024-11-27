import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("상가 입지분석 어시스턴트 🏪")
    
    # API 키 입력
    api_key = st.text_input("Gemini API 키를 입력하세요", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("상가 관련 PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file:
            pdf_content = read_pdf(uploaded_file)
            st.success("PDF 파일이 성공적으로 업로드되었습니다!")
            
            # 채팅 인터페이스
            if "messages" not in st.session_state:
                st.session_state.messages = []
                
            # 이전 메시지 표시
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # 사용자 입력
            if prompt := st.chat_input("질문을 입력하세요"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Gemini 모델 설정 및 응답 생성
                model = genai.GenerativeModel('gemini-pro')
                context = f"""
                다음은 상가 관련 문서입니다:
                {pdf_content}
                
                위 문서를 바탕으로 다음 질문에 답변해주세요: {prompt}
                """
                
                response = model.generate_content(context)
                
                # 응답 표시
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

if __name__ == "__main__":
    main()
