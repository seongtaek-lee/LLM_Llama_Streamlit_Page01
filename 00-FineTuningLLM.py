import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import load_prompt
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="SETBOX Model Llama3.1 💬", page_icon="💬")
st.title("SETBOX Model Llama3.1 💬")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "prompt" not in st.session_state:
    # 기본 프롬프트 설정
    st.session_state["prompt"] = ChatPromptTemplate.from_template(
        "Below is a logistics task and relevant context. Write a response that analyzes the problem.\n\n"
        "### Task:\n{question}\n\n"
        "### Context:\n"
        "1 SETBOX operations involve coordination between HIMS and ECS.\n\n"
        "2 SETBOXRACK operations involve coordination between HIMS and LEO.\n\n"
        "3 Recent delays have been reported in the 1st and 2nd floor dispatch process.\n\n"
        "4 SETBOX raise to A61(E-Andon).\n\n"
        "### Response:"
    )


def print_history():
    for msg in st.session_state["messages"]:
        st.chat_message(msg.role).write(msg.content)


def add_history(role, content):
    st.session_state["messages"].append(ChatMessage(role=role, content=content))


# 체인을 생성합니다.
def create_chain(prompt):
    chain = (
        prompt | ChatOllama(model="Llma3-HMGICS-SETBOX-Q8:latest") | StrOutputParser()
    )
    return chain


with st.sidebar:
    clear_btn = st.button("Reset the chat box")
    # tab1, tab2 = st.tabs(["Prompt", "freeset"])
    # # 기본 프롬프트 설정
    # prompt = """"""
    # user_text_prompt = tab1.text_area("Prompt", value=prompt)
    # user_text_apply_btn = tab1.button("Prompt apply", key="apply1")
    # if user_text_apply_btn:
    #     tab1.markdown(f"✅ Prompt complete")
    #     prompt_template = user_text_prompt
    #     prompt = PromptTemplate.from_template(prompt_template)
    #     st.session_state["chain"] = create_chain(prompt)

    # user_selected_prompt = tab2.selectbox("free set ", ["sns", "번역", "요약"])
    # user_selected_apply_btn = tab2.button("Prompt Apply", key="apply2")
    # if user_selected_apply_btn:
    #     tab2.markdown(f"✅ Prompt complete")
    #     prompt = load_prompt(f"prompts/{user_selected_prompt}.yaml", encoding="utf8")
    #     st.session_state["chain"] = create_chain(prompt)

if clear_btn:
    st.session_state["messages"].clear()

print_history()

# 체인이 세션 상태에 없으면 생성
if "chain" not in st.session_state:
    st.session_state["chain"] = create_chain(st.session_state["prompt"])

if user_input := st.chat_input():
    add_history("user", user_input)
    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        chat_container = st.empty()

        stream_response = st.session_state["chain"].stream(
            {"question": user_input}
        )  # 문서에 대한 질의
        ai_answer = ""
        for chunk in stream_response:
            ai_answer += chunk
            chat_container.markdown(ai_answer)
        add_history("ai", ai_answer)
